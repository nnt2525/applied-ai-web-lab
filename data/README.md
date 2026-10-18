# Educational data

All records in this directory were created for the repository. They do not
represent real customers, businesses or market findings.

| File | Contents |
|---|---|
| `support_tickets.jsonl` | 160 hand-authored Thai/English tickets; `id`, `label`, `family`, `split`, `language`, `text` |
| `unknown_tickets.json` | Six development and six heldout unrelated requests used to evaluate abstention |
| `sales.csv` | 2,196 synthetic daily product/channel aggregates, 2026-04-01 through 2026-09-30 |
| `metrics.json` | Reproducible classifier, unknown rejection and demand regression metrics |

Sales fields: `date` (ISO calendar date), `category`, `product`, `units`
(nonnegative integer), `unit_price` (THB), `revenue` (THB, units × price), `cost`
(THB, units × invented unit cost), and `channel` (`Online` or `Store`). Cost is
cost of goods only; the dashboard's gross profit excludes operating expenses.

Generate the data and model exports with `python -m ml.train` from the repository
root. Read [the model cards](../docs/MODEL_CARD.md) for split strategy, methods,
metrics and limitations. No external data downloads or API keys are required.
