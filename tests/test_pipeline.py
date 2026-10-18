"""Meaningful invariants for reproducibility, leakage, metrics and inference."""
from collections import Counter
from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import tempfile
import unittest

from ml.datasets import ticket_rows
from ml.forecast import errors, examples, fit_ridge, predict as forecast_predict, train_forecast
from ml.train import CLASSES, classification_metrics, features, fit, inference_fixtures, make_sales, normalize, predict, run


class PipelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = ticket_rows()
        cls.train = [row for row in cls.rows if row["split"] == "train"]
        cls.model = fit(cls.train)

    def test_families_and_normalized_texts_do_not_cross_splits(self):
        for key in ["family", "text"]:
            owners = {}
            for row in self.rows:
                value = normalize(row[key])
                self.assertEqual(owners.setdefault(value, row["split"]), row["split"])
        self.assertEqual(Counter(row["split"] for row in self.rows), {"train": 96, "dev": 32, "test": 32})

    def test_training_vocabulary_excludes_unseen_test_ngrams(self):
        # A deliberately unique heldout marker cannot influence fitted features.
        unique = "🧬🛰🪼"
        before = fit(self.train)
        heldout = [{"text": unique, "label": "account", "split": "test"}]
        self.assertTrue(all(gram not in before["vocabulary"] for gram in features(heldout[0]["text"])))
        self.assertEqual(before, self.model)

    def test_normalization_ngram_counts_and_bilingual_inference(self):
        self.assertEqual(normalize("  ＡＡ\nB  "), "aa b")
        self.assertEqual(features("aaaa")["aa"], 3)
        for text, label in [("Please reset my account password", "account"),
                            ("บัตรถูกหักเงินซ้ำสองครั้ง", "billing"),
                            ("พัสดุจัดส่งล่าช้า", "delivery"),
                            ("The website crashes with an error", "technical")]:
            result = predict(self.model, text)
            self.assertEqual(result["top_class"], label)
            self.assertAlmostEqual(sum(result["posterior"].values()), 1)

    def test_empty_unseen_input_abstains_when_threshold_enabled(self):
        model = dict(self.model, thresholds={"min_coverage": 0.2, "min_top_posterior": 0.8})
        for text in ["", "a", "🧬🛰🪼"]:
            self.assertEqual(predict(model, text)["label"], "unknown")

    def test_confusion_matrix_totals_and_macro_f1(self):
        metric = classification_metrics(self.model, self.train)
        self.assertEqual(sum(sum(row.values()) for row in metric["confusion_matrix"].values()), len(self.train))
        self.assertAlmostEqual(metric["macro_f1"], sum(row["f1"] for row in metric["per_class"].values()) / len(CLASSES), places=3)
        self.assertEqual(metric["accepted"] + metric["abstained"], len(self.train))

    def test_sales_reproducibility_arithmetic_and_interval(self):
        sales = make_sales()
        self.assertEqual(sales, make_sales())
        self.assertEqual(sales[0]["date"], "2026-04-01")
        self.assertEqual(sales[-1]["date"], "2026-09-30")
        self.assertEqual(len(sales), 183 * 6 * 2)
        for row in sales:
            self.assertGreaterEqual(row["units"], 0)
            self.assertEqual(row["revenue"], round(row["units"] * row["unit_price"], 2))

    def test_forecast_chronology_and_train_only_scaling(self):
        sales = make_sales()
        rows = examples(sales)
        model, predictions, metrics = train_forecast(sales)
        self.assertEqual(metrics["split_counts"], {"train": 120, "dev": 28, "test": 28})
        self.assertLess(metrics["periods"]["train"]["end"], metrics["periods"]["dev"]["start"])
        self.assertLess(metrics["periods"]["dev"]["end"], metrics["periods"]["test"]["start"])
        for column, mean in enumerate(model["means"]):
            self.assertAlmostEqual(mean, sum(row["features"][column] for row in rows[:120]) / 120)
        test = [row for row in predictions if row["split"] == "test"]
        self.assertEqual(metrics["test"], errors([row["actual"] for row in test], [row["prediction"] for row in test]))
        self.assertTrue(all(forecast_predict(model, row) >= 0 for row in rows))

    def test_regression_can_recover_a_linear_signal(self):
        rows = [{"features": [index, 0, 0, 0, 0, 0, 0, 0], "units": 2 * index + 3} for index in range(20)]
        model = fit_ridge(rows, 0.0001)
        self.assertAlmostEqual(forecast_predict(model, {"features": [30, 0, 0, 0, 0, 0, 0, 0]}), 63, places=2)

    def test_export_roundtrip_and_record_counts(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory)
            with redirect_stdout(io.StringIO()):
                model, metrics = run(destination)
            exported = json.loads((destination / "web/assets/models/support-model.json").read_text(encoding="utf-8"))
            self.assertEqual(model, exported)
            self.assertEqual(predict(model, "reset my account password"), predict(exported, "reset my account password"))
            stored = json.loads((destination / "web/assets/data/metrics.json").read_text(encoding="utf-8"))
            self.assertEqual(metrics, stored)
            fixtures = json.loads((destination / "tests/inference-fixtures.json").read_text(encoding="utf-8"))
            self.assertEqual(fixtures, inference_fixtures(model))
            self.assertEqual(len(fixtures), 12)
            self.assertTrue(any(row["abstained"] for row in fixtures))
            self.assertEqual(len((destination / "data/support_tickets.jsonl").read_text(encoding="utf-8").splitlines()), 160)


if __name__ == "__main__":
    unittest.main()
