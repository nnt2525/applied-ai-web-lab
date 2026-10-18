"""Reproduce fixtures, fit a character Naive Bayes model, and export browser data.

Run from the repository root: python -m ml.train
Only the Python standard library is required.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import date, timedelta
import csv
import hashlib
import json
import math
from pathlib import Path
import random
import re
import unicodedata

from .datasets import UNKNOWN, ticket_rows
from .forecast import train_forecast

ROOT = Path(__file__).resolve().parents[1]
CLASSES = ["account", "billing", "delivery", "technical"]


def normalize(text):
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", text).lower()).strip()[:1000]


def features(text):
    text = normalize(text)
    return Counter(text[index:index + size] for size in range(2, 5)
                   for index in range(len(text) - size + 1))


def fit(rows, alpha=0.5):
    counts = {label: Counter() for label in CLASSES}
    docs = Counter()
    frequency = Counter()
    for row in rows:
        grams = features(row["text"])
        docs[row["label"]] += 1
        counts[row["label"]].update(grams)
        frequency.update(grams.keys())
    vocabulary = sorted(gram for gram, count in frequency.items() if count >= 2)
    likelihoods = {}
    fallback = {}
    for label in CLASSES:
        denominator = sum(counts[label][gram] for gram in vocabulary) + alpha * len(vocabulary)
        fallback[label] = round(math.log(alpha / denominator), 8)
        likelihoods[label] = {gram: round(math.log((counts[label][gram] + alpha) / denominator), 8)
                                for gram in vocabulary if counts[label][gram]}
    return {"schema_version": 1, "model_type": "char-ngram-multinomial-naive-bayes",
            "classes": CLASSES, "ngram_range": [2, 4],
            "normalization": "NFKC + lowercase + whitespace collapse", "text_limit": 1000,
            "alpha": alpha, "min_document_frequency": 2, "vocabulary": vocabulary,
            "priors": {label: round(math.log(docs[label] / len(rows)), 8) for label in CLASSES},
            "likelihoods": likelihoods, "default_log_likelihood": fallback,
            "thresholds": {"min_coverage": 0, "min_top_posterior": 0},
            "training_examples": len(rows), "data_kind": "hand-authored educational synthetic examples",
            "posterior_note": "Uncalibrated Naive Bayes posterior, not probability of correctness."}


def predict(model, text):
    counts = features(text)
    vocabulary = set(model["vocabulary"])
    known = {gram: count for gram, count in counts.items() if gram in vocabulary}
    coverage = sum(known.values()) / max(1, sum(counts.values()))
    scores = {}
    for label in model["classes"]:
        likelihoods = model["likelihoods"][label]
        default = model["default_log_likelihood"][label]
        scores[label] = model["priors"][label] + sum(count * likelihoods.get(gram, default)
                                                   for gram, count in known.items())
    maximum = max(scores.values())
    weights = {label: math.exp(score - maximum) for label, score in scores.items()}
    total = sum(weights.values())
    posterior = {label: weight / total for label, weight in weights.items()}
    top = max(posterior, key=posterior.get)
    thresholds = model["thresholds"]
    abstain = coverage < thresholds["min_coverage"] or posterior[top] < thresholds["min_top_posterior"]
    return {"label": "unknown" if abstain else top, "top_class": top,
            "posterior": posterior, "coverage": coverage, "abstained": abstain}


def classification_metrics(model, rows):
    confusion = {label: {prediction: 0 for prediction in CLASSES} for label in CLASSES}
    accepted = correct_accepted = 0
    for row in rows:
        result = predict(model, row["text"])
        confusion[row["label"]][result["top_class"]] += 1
        accepted += not result["abstained"]
        correct_accepted += not result["abstained"] and result["top_class"] == row["label"]
    correct = sum(confusion[label][label] for label in CLASSES)
    per_class = {}
    for label in CLASSES:
        tp = confusion[label][label]
        precision = tp / max(1, sum(confusion[other][label] for other in CLASSES))
        recall = tp / max(1, sum(confusion[label].values()))
        f1 = 2 * precision * recall / max(1e-12, precision + recall)
        per_class[label] = {"precision": round(precision, 4), "recall": round(recall, 4), "f1": round(f1, 4)}
    return {"n": len(rows), "accuracy": round(correct / len(rows), 4),
            "macro_f1": round(sum(value["f1"] for value in per_class.values()) / len(CLASSES), 4),
            "per_class": per_class, "confusion_matrix": confusion,
            "accepted": accepted, "abstained": len(rows) - accepted,
            "acceptance_rate": round(accepted / len(rows), 4),
            "selective_accuracy": round(correct_accepted / accepted, 4) if accepted else None,
            "correct_accepted_rate": round(correct_accepted / len(rows), 4)}


def choose_thresholds(model, dev):
    known = [(row["label"], predict(model, row["text"])) for row in dev]
    unknown = [predict(model, text) for text in UNKNOWN["dev"]]
    best = None
    for coverage in [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7]:
        for posterior in [0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.99]:
            def accepts(result):
                return result["coverage"] >= coverage and max(result["posterior"].values()) >= posterior
            known_score = sum(accepts(result) and result["top_class"] == label for label, result in known) / len(known)
            unknown_score = sum(not accepts(result) for result in unknown) / len(unknown)
            # Equal weight to correct in-domain routing and unknown rejection.
            # In a tie prefer lower thresholds, preserving more known requests.
            candidate = (0.5 * (known_score + unknown_score), -coverage, -posterior)
            if best is None or candidate > best[0]:
                best = (candidate, coverage, posterior, known_score, unknown_score)
    model["thresholds"] = {"min_coverage": best[1], "min_top_posterior": best[2]}
    return {"objective": "0.5 * (correct accepted in-domain rate + unknown rejection rate)",
            "balanced_dev_score": round(best[0][0], 4), "dev_correct_accepted_rate": round(best[3], 4),
            "dev_unknown_rejection_rate": round(best[4], 4), "selected_on": "dev only",
            "coverage_grid": [round(0.05 * index, 2) for index in range(1, 15)],
            "posterior_grid": [0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.99]}


def unknown_metrics(model, texts):
    results = [predict(model, text) for text in texts]
    rejected = sum(result["abstained"] for result in results)
    return {"n": len(texts), "rejected": rejected, "false_accepts": len(texts) - rejected,
            "rejection_rate": round(rejected / len(texts), 4),
            "examples": [{"text": text, "label": result["label"], "coverage": round(result["coverage"], 4),
                           "top_posterior": round(max(result["posterior"].values()), 4)}
                          for text, result in zip(texts, results)]}


PRODUCTS = [
    ("Accessories", "USB-C Hub", 1290.0, 670.0, 5),
    ("Accessories", "Laptop Stand", 890.0, 390.0, 7),
    ("Audio", "Wireless Headphones", 2490.0, 1420.0, 4),
    ("Audio", "Mini Speaker", 1590.0, 820.0, 4),
    ("Desk", "Mechanical Keyboard", 1990.0, 1080.0, 5),
    ("Desk", "Desk Lamp", 790.0, 350.0, 8),
]


def make_sales(seed=20261019):
    rng = random.Random(seed)
    start, end = date(2026, 4, 1), date(2026, 9, 30)
    rows = []
    day = start
    while day <= end:
        elapsed = (day - start).days
        weekend = 1.22 if day.weekday() >= 5 else 1.0
        trend = 1 + elapsed * 0.0018
        seasonal = 1 + 0.12 * math.sin(2 * math.pi * elapsed / 30)
        promotion = 1.25 if day.day in [9, 10, 25] else 1
        for category, product, price, cost, demand in PRODUCTS:
            for channel, share in [("Online", 0.65), ("Store", 0.35)]:
                noise = max(0.2, rng.gauss(1.0, 0.22))
                units = max(0, round(demand * weekend * trend * seasonal * promotion * share * noise))
                unit_price = round(price * (0.9 if promotion > 1 else 1), 2)
                rows.append({"date": day.isoformat(), "category": category, "product": product,
                             "units": units, "unit_price": unit_price, "revenue": round(units * unit_price, 2),
                             "cost": round(units * cost, 2), "channel": channel})
        day += timedelta(days=1)
    return rows


def sales_summary(rows):
    revenue = sum(row["revenue"] for row in rows)
    cost = sum(row["cost"] for row in rows)
    return {"kind": "synthetic retail transactions aggregated by day/product/channel",
            "seed": 20261019, "start_date": rows[0]["date"], "end_date": rows[-1]["date"],
            "days": len(set(row["date"] for row in rows)), "rows": len(rows),
            "currency": "THB", "revenue": round(revenue, 2), "cost": round(cost, 2),
            "gross_profit": round(revenue - cost, 2), "units": sum(row["units"] for row in rows),
            "categories": sorted(set(row["category"] for row in rows)),
            "products": sorted(set(row["product"] for row in rows)), "channels": ["Online", "Store"],
            "caveat": "Generated trends, seasonality and promotions are assumptions, not market evidence."}


def write_json(path, value, compact=False):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, separators=(",", ":") if compact else None,
                               indent=None if compact else 2) + "\n", encoding="utf-8")


def inference_fixtures(model):
    """Cross-language conformance cases; regenerated from the fitted model.

    Browser validation rejects blank input and text beyond its character limit;
    fixtures exercise valid nonblank input only, including an abstained 1-char
    input and non-BMP characters to catch UTF-16 slicing mistakes.
    """
    examples = [
        ("train-en-account", "I forgot my account password and need a reset"),
        ("train-th-billing", "ขอใบเสร็จรับเงินและใบแจ้งหนี้"),
        ("heldout-en-delivery", "When will the warehouse dispatch my package for delivery"),
        ("heldout-th-technical", "แอปส่งออกไฟล์ไม่ได้และแจ้งข้อผิดพลาด"),
        ("heldout-en-account", "I cannot create a new user account"),
        ("heldout-th-billing", "ยอดชำระเงินนี้แบ่งจ่ายรายเดือนได้ไหม"),
        ("unknown-en-false-accept", "Who won the football match yesterday"),
        ("unknown-th-abstain", "แมวชอบนอนวันละกี่ชั่วโมง"),
        ("nfkc-fullwidth", "Ｐｌｅａｓｅ ｒｅｓｅｔ ｍｙ ａｃｃｏｕｎｔ ｐａｓｓｗｏｒｄ"),
        ("unicode-emoji", "🛠️ แอปค้างและเว็บไซต์ขึ้นข้อผิดพลาด 🚀"),
        ("single-character", "ก"),
        ("whitespace-lowercase", "  THE\tWEBSITE\nCRASHES WITH AN ERROR\u00a0 "),
    ]
    fixtures = []
    for identity, text in examples:
        result = predict(model, text)
        fixtures.append({"id": identity, "text": text, "top_class": result["top_class"],
                         "posterior": result["posterior"], "coverage": result["coverage"],
                         "abstained": result["abstained"]})
    return fixtures


def run(output=ROOT):
    rows = ticket_rows()
    splits = {split: [row for row in rows if row["split"] == split] for split in ["train", "dev", "test"]}
    model = fit(splits["train"])
    threshold_selection = choose_thresholds(model, splits["dev"])
    majority = Counter(row["label"] for row in splits["train"]).most_common(1)[0][0]
    baseline_accuracy = sum(row["label"] == majority for row in splits["test"]) / len(splits["test"])
    # Always predicting the training-majority label gives F1 .4 for that class
    # on this balanced test; the other three classes have zero F1.
    baseline_precision = baseline_accuracy
    baseline_f1 = 2 * baseline_precision / (1 + baseline_precision) / len(CLASSES)
    metrics = {"schema_version": 1, "classifier": {
        "dataset": "Hand-authored bilingual support tickets, synthetic, 40 semantic families",
        "data_sha256": hashlib.sha256(json.dumps(rows, ensure_ascii=False, sort_keys=True).encode()).hexdigest(),
        "classes": CLASSES, "split_strategy": "Family-disjoint authored train/dev/test; all paraphrases of one semantic family remain together",
        "split_counts": {split: len(values) for split, values in splits.items()},
        "family_counts": {split: len(set(row["family"] for row in values)) for split, values in splits.items()},
        "class_counts": {split: dict(Counter(row["label"] for row in values)) for split, values in splits.items()},
        "language_counts": dict(Counter(row["language"] for row in rows)), "vocabulary_size": len(model["vocabulary"]),
        "thresholds": model["thresholds"], "threshold_selection": threshold_selection,
        "dev": classification_metrics(model, splits["dev"]), "test": classification_metrics(model, splits["test"]),
        "majority_baseline": {"label": majority, "accuracy": round(baseline_accuracy, 4), "macro_f1": round(baseline_f1, 4)},
        "unknown_dev": unknown_metrics(model, UNKNOWN["dev"]), "unknown_test": unknown_metrics(model, UNKNOWN["test"]),
        "limitations": ["Tiny hand-authored synthetic dataset; does not establish performance on real customers.",
                        "Semantic families are disjoint but share author style and domain keywords.",
                        "Naive Bayes posteriors are uncalibrated and often overconfident.",
                        "Unknown rejection is a heuristic tuned on only six dev examples.",
                        "Only four intents, Thai/English, single-label routing; no action is executed."]}}
    sales = make_sales()
    metrics["sales"] = sales_summary(sales)
    demand_model, forecast_rows, metrics["forecast"] = train_forecast(sales)
    write_json(output / "web/assets/models/support-model.json", model, compact=True)
    write_json(output / "tests/inference-fixtures.json", inference_fixtures(model))
    write_json(output / "web/assets/models/demand-model.json", demand_model)
    write_json(output / "web/assets/data/forecast.json", forecast_rows)
    write_json(output / "web/assets/data/sales.json", sales, compact=True)
    write_json(output / "web/assets/data/metrics.json", metrics)
    write_json(output / "data/metrics.json", metrics)
    write_json(output / "data/unknown_tickets.json", UNKNOWN)
    (output / "data").mkdir(parents=True, exist_ok=True)
    with (output / "data/support_tickets.jsonl").open("w", encoding="utf-8", newline="\n") as stream:
        for row in rows:
            stream.write(json.dumps(row, ensure_ascii=False) + "\n")
    with (output / "data/sales.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(sales[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(sales)
    print(json.dumps({"classifier": metrics["classifier"]["test"], "thresholds": model["thresholds"],
                      "unknown_test": metrics["classifier"]["unknown_test"], "sales": metrics["sales"],
                      "forecast": metrics["forecast"]}, indent=2, ensure_ascii=False))
    return model, metrics


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT)
    run(parser.parse_args().output)
