"""Small ridge regression with a chronological holdout, using standard library.

The task is daily total units, predicted one day at a time with observed lag-7
units. This is retrospective one-step evaluation, not an independent 28-day
forecast: each test date can use the actual value seven days earlier.
"""
from collections import defaultdict
from datetime import date
import math


FEATURES = ["trend_day", "is_weekend", "sin_week", "cos_week", "sin_30", "cos_30", "is_promotion", "lag_7_units"]


def solve(matrix, vector):
    """Gaussian elimination with partial pivoting for a tiny dense system."""
    width = len(vector)
    augmented = [row[:] + [value] for row, value in zip(matrix, vector)]
    for column in range(width):
        pivot = max(range(column, width), key=lambda index: abs(augmented[index][column]))
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        divisor = augmented[column][column]
        if abs(divisor) < 1e-12:
            raise ValueError("Singular regression system")
        augmented[column] = [value / divisor for value in augmented[column]]
        for row in range(width):
            if row == column:
                continue
            multiplier = augmented[row][column]
            augmented[row] = [left - multiplier * right for left, right in zip(augmented[row], augmented[column])]
    return [row[-1] for row in augmented]


def examples(sales):
    totals = defaultdict(int)
    for row in sales:
        totals[row["date"]] += row["units"]
    days = sorted(totals)
    rows = []
    for index in range(7, len(days)):
        day = date.fromisoformat(days[index])
        rows.append({"date": days[index], "units": totals[days[index]],
                     "features": [index, int(day.weekday() >= 5), math.sin(2 * math.pi * index / 7),
                                  math.cos(2 * math.pi * index / 7), math.sin(2 * math.pi * index / 30),
                                  math.cos(2 * math.pi * index / 30), int(day.day in [9, 10, 25]),
                                  totals[days[index - 7]]]})
    return rows


def fit_ridge(rows, alpha):
    columns = list(zip(*(row["features"] for row in rows)))
    means = [sum(column) / len(column) for column in columns]
    scales = [math.sqrt(sum((value - mean) ** 2 for value in column) / len(column)) or 1
              for mean, column in zip(means, columns)]
    design = [[1] + [(value - mean) / scale for value, mean, scale in zip(row["features"], means, scales)]
              for row in rows]
    width = len(FEATURES) + 1
    gram = [[sum(row[left] * row[right] for row in design) + (alpha if left == right and left else 0)
             for right in range(width)] for left in range(width)]
    target = [sum(vector[column] * row["units"] for vector, row in zip(design, rows)) for column in range(width)]
    weights = solve(gram, target)
    return {"schema_version": 1, "model_type": "ridge-linear-regression", "target": "daily_total_units",
            "feature_names": FEATURES, "means": [round(value, 10) for value in means],
            "scales": [round(value, 10) for value in scales], "intercept": round(weights[0], 10),
            "coefficients": [round(value, 10) for value in weights[1:]],
            "alpha": alpha, "scaling_fit": "train only", "clip_min": 0}


def predict(model, row):
    standardized = [(value - mean) / scale for value, mean, scale in zip(row["features"], model["means"], model["scales"])]
    return max(0, model["intercept"] + sum(weight * value for weight, value in zip(model["coefficients"], standardized)))


def errors(actual, predicted):
    return {"mae": round(sum(abs(a - p) for a, p in zip(actual, predicted)) / len(actual), 4),
            "rmse": round(math.sqrt(sum((a - p) ** 2 for a, p in zip(actual, predicted)) / len(actual)), 4)}


def train_forecast(sales):
    rows = examples(sales)
    train, dev, test = rows[:-56], rows[-56:-28], rows[-28:]
    candidates = []
    for alpha in [0.01, 0.1, 1, 10, 100]:
        model = fit_ridge(train, alpha)
        dev_errors = errors([row["units"] for row in dev], [predict(model, row) for row in dev])
        candidates.append((dev_errors["mae"], alpha, model))
    _, alpha, model = min(candidates, key=lambda candidate: (candidate[0], candidate[1]))
    model["training_period"] = {"start": train[0]["date"], "end": train[-1]["date"], "n": len(train)}
    predictions = []
    for split, records in [("train", train), ("dev", dev), ("test", test)]:
        for row in records:
            predictions.append({"date": row["date"], "split": split, "actual": row["units"],
                                "prediction": round(predict(model, row), 4), "baseline": row["features"][-1]})
    test_actual = [row["units"] for row in test]
    metric = {"model": "Ridge linear regression", "target": "daily total units",
              "split_strategy": "Chronological: 120 train, 28 dev, 28 test after 7-day lag warm-up",
              "split_counts": {"train": len(train), "dev": len(dev), "test": len(test)},
              "periods": {split: {"start": records[0]["date"], "end": records[-1]["date"]}
                          for split, records in [("train", train), ("dev", dev), ("test", test)]},
              "selected_alpha": alpha, "alpha_selection": "Lowest dev MAE; test never used for fitting or selection",
              "scaling": "Means and population standard deviations fit on train only; no refit after dev selection",
              "dev": errors([row["units"] for row in dev], [predict(model, row) for row in dev]),
              "test": errors(test_actual, [predict(model, row) for row in test]),
              "last_week_baseline": errors(test_actual, [row["features"][-1] for row in test]),
              "limitations": ["Synthetic demand contains an intentionally learnable trend and seasonality.",
                              "One-step retrospective evaluation uses observed lag-7 units; not a 28-day recursive forecast.",
                              "Future calendar and promotion flags are assumed known.",
                              "No prediction intervals, external shocks, stockouts, or real retail validation."]}
    return model, predictions, metric
