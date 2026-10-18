# Model cards and evaluation

This repository contains two small fitted models. All training and evaluation
data are synthetic educational examples created for this repository. No customer
records, company sales, personal information, or paid AI API are used.

Reproduce all artifacts from the repository root:

```sh
python -m ml.train
python -m unittest discover -s tests -v
```

The pipeline requires Python 3.10+ and the standard library only. The exported
JSON files are checked into the repository so that the website runs independently
of Python. Training is deterministic; no random train/test shuffling occurs.

## Bilingual support-ticket router

**Intended use:** demonstrate text preprocessing, model fitting, evaluation,
browser inference and honest communication of limitations in an internship
portfolio. The model proposes one of `account`, `billing`, `delivery` or
`technical`, or abstains with `unknown`. It does not execute account, financial
or support actions.

**Method:** Multinomial Naive Bayes on unpadded character 2-, 3- and 4-gram
counts. Input is Unicode NFKC normalized, lowercased, trimmed and whitespace
collapsed, then limited to 1,000 characters. Vocabulary requires a gram to appear
in at least two training documents. Additive smoothing alpha is 0.5. Priors and
likelihoods are estimated from training records only. Unknown grams are omitted
from the score rather than assigned a class-specific unseen token probability.

**Data:** `data/support_tickets.jsonl` contains 160 hand-authored examples: 80
English and 80 Thai, 40 examples per class. There are 40 semantic families, each
with two English and two Thai paraphrases. A family is assigned entirely to one
split, preserving paraphrase and translation groups:

| Split | Examples | Families | Examples per class |
|---|---:|---:|---:|
| Train | 96 | 24 | 24 |
| Development | 32 | 8 | 8 |
| Test | 32 | 8 | 8 |

This is a manually authored family split, not a random sample of a real support
population. All splits share one authoring process and easy domain keywords.
Grouping removes direct paraphrase leakage but cannot remove author-style bias.

**Abstention:** coverage is the count of known gram occurrences divided by all
gram occurrences. A request is rejected when coverage is below 0.35 or its top
Naive Bayes posterior is below 0.8. Those thresholds are selected on the 32 known
development examples and six separately authored unknown development examples.
The grid maximizes the mean of correct accepted in-domain rate and unknown
rejection rate; ties select lower thresholds. Test examples are not used to fit
the model or choose thresholds. Test results were inspected after this pipeline
was fixed and are reported unchanged, including failed unknown rejection.

The softmax output is an **uncalibrated Naive Bayes posterior**. It is not an
estimated probability that the prediction is correct. Overlapping grams violate
the conditional independence assumption and can make that posterior extremely
close to 1 even for unrelated text.

**Heldout results** (see generated `data/metrics.json`):

| Measure | Value |
|---|---:|
| Closed-set test accuracy, before abstention | 1.0000 (32/32) |
| Closed-set test macro-F1, before abstention | 1.0000 |
| Training-majority baseline accuracy | 0.2500 |
| Training-majority baseline macro-F1 | 0.1000 |
| In-domain acceptance rate | 0.9688 (31/32) |
| Accuracy among accepted in-domain examples | 1.0000 (31/31) |
| Unknown test rejection rate | 0.5000 (3/6) |
| Unknown test false accepts | 3/6 |

The closed-set confusion matrix has eight correct predictions in each class and
zero off-diagonal predictions. This high score is expected on a tiny authored
dataset and **does not establish accuracy on real users**. In contrast, the
unknown test exposes a substantial failure: unrelated football, guitar and
travel requests can be accepted with a high posterior. The UI should surface
that limitation alongside the synthetic in-domain score.

Before any real use, collect consented and deidentified domain data, define an
annotation policy, include ambiguous and mixed intents, use independent authors
and a fresh locked test set, and evaluate dialect, spelling and class imbalance.
Compare stronger models and calibrated uncertainty against this simple baseline.
Treat sensitive or automated actions as a separate product and review problem.

## Synthetic retail demand regression

**Data:** 183 days from 2026-04-01 through 2026-09-30. Each day contains six
products in three categories and two channels: 2,196 day/product/channel rows.
Seed `20261019` creates nonnegative integer units from an explicit upward trend,
weekend effect, 30-day seasonality, scheduled promotion days and Gaussian noise.
Prices, unit costs and product demand levels are invented. Revenue is units
times unit price; cost is units times fixed product unit cost. The dataset has
no missing values, returns, taxes, stockouts or customer identities.

**Method:** ridge linear regression predicts daily total units. Features are
day index, weekend indicator, sine/cosine for 7-day and 30-day cycles, known
promotion indicator, and observed units seven days earlier. Input columns are
standardized using training means and population standard deviations only.
The intercept is not regularized; coefficients are fit with a small explicit
linear-system solver. Predictions are clipped at zero.
Exported means, scales, coefficients and intercept are rounded to ten decimal
places to avoid insignificant platform math differences. All evaluation and
browser predictions use those same rounded parameters.

After seven warm-up days, splits are chronological:

| Split | Dates | Days |
|---|---|---:|
| Train | 2026-04-08 to 2026-08-05 | 120 |
| Development | 2026-08-06 to 2026-09-02 | 28 |
| Test | 2026-09-03 to 2026-09-30 | 28 |

Alpha is selected by development MAE from `[0.01, 0.1, 1, 10, 100]`; selected
alpha is 100. Neither coefficients nor scaling are refit after selection.

| Test predictor | MAE, units/day | RMSE, units/day |
|---|---:|---:|
| Ridge model | 3.8833 | 4.9542 |
| Same day last week baseline | 7.8571 | 9.4188 |

This is **one-step retrospective evaluation** with observed lag-7 values for
each date. When an earlier test date becomes history, its actual value can be
used seven days later. The exported 28 test predictions are therefore not a
single 28-day recursive forecast issued before September. Calendar and promotion
flags are assumed known. The generator deliberately includes learnable patterns;
better synthetic error does not demonstrate commercial demand forecasting skill.
No prediction intervals or deployment claims are provided.

## Browser artifact contract

- `web/assets/models/support-model.json`: `classes`, `vocabulary`, `priors`
  (natural-log class priors), sparse `likelihoods[class][gram]` (natural-log
  likelihoods), `default_log_likelihood[class]` for known vocabulary grams absent
  in that class, and dev-selected `thresholds`. Count each known gram and sum
  count × log likelihood plus prior. Apply a numerically stable softmax for
  posterior display. All classes share the same vocabulary. Export version is 1.
- Character grams use Unicode code points. JavaScript can use `Array.from(text)`
  before slicing to match Python for characters outside the basic multilingual
  plane. NFKC, whitespace and character limit normalization precede features.
- `web/assets/models/demand-model.json`: feature order, train-only means/scales,
  intercept, coefficients and selected alpha for reproducing daily predictions.
- `web/assets/data/forecast.json`: one record per modeled day with `date`,
  `split`, `actual`, `prediction`, and same-weekday `baseline`.
- `web/assets/data/sales.json`: records with `date`, `category`, `product`,
  `units`, `unit_price`, `revenue`, `cost` and `channel`.
- `web/assets/data/metrics.json` and `data/metrics.json`: identical evaluation
  records including counts, confusion matrix, baselines, abstention and caveats.
- `tests/inference-fixtures.json`: 12 Python reference predictions regenerated by
  training, including heldout Thai/English, unknown, fullwidth, emoji and short
  input cases. Browser `label` denotes the top class even when abstained; compare
  it to fixture `top_class`, and compare the separate abstention flag.

The browser runs inference locally from the exported classifier. No ticket text
needs to be sent to a remote service. Predictions are demonstrations, and users
should enter sample text rather than real private records.
