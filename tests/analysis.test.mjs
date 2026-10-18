import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { filterRows, summarize, groupRows, toCSV } from '../web/assets/analysis.js';
import { predictDemand } from '../web/assets/demand.js';

const rows = JSON.parse(await readFile(new URL('../web/assets/data/sales.json', import.meta.url), 'utf8'));
const metrics = JSON.parse(await readFile(new URL('../web/assets/data/metrics.json', import.meta.url), 'utf8'));
test('browser aggregates reproduce the Python pipeline totals', () => {
  const result = summarize(rows);
  assert.equal(result.revenue, metrics.sales.revenue);
  assert.equal(result.profit, metrics.sales.gross_profit);
  assert.equal(result.units, metrics.sales.units);
  assert.equal(result.records, 2196);
});
test('period, category and channel filters compose without altering source rows', () => {
  const result = filterRows(rows, { month: '2026-04', category: 'Audio', channel: 'Online' });
  assert.equal(result.length, 60);
  assert.ok(result.every(row => row.date.startsWith('2026-04') && row.category === 'Audio' && row.channel === 'Online'));
  assert.equal(rows.length, 2196);
});
test('category grouping conserves revenue and units', () => {
  const groups = groupRows(rows, 'category');
  assert.equal(groups.reduce((sum, row) => sum + row.revenue, 0), summarize(rows).revenue);
  assert.equal(groups.reduce((sum, row) => sum + row.units, 0), summarize(rows).units);
});
test('empty selections produce finite, zeroed KPIs', () => {
  assert.deepEqual(summarize([]), { revenue: 0, cost: 0, units: 0, profit: 0, margin: 0, records: 0 });
  assert.deepEqual(filterRows(rows, { category: 'missing' }), []);
});
test('CSV preserves quotes and commas and neutralizes spreadsheet formulas', () => {
  const csv = toCSV([{ ...rows[0], product: 'A "quoted", name', category: '=DANGEROUS()' }]);
  assert.ok(csv.includes('"A ""quoted"", name"'));
  assert.ok(csv.includes("'=DANGEROUS()"));
  assert.equal(toCSV(rows).split('\r\n').length, rows.length + 1);
});

test('live browser ridge inference matches all Python forecast exports', async () => {
  const model = JSON.parse(await readFile(new URL('../web/assets/models/demand-model.json', import.meta.url), 'utf8'));
  const forecasts = JSON.parse(await readFile(new URL('../web/assets/data/forecast.json', import.meta.url), 'utf8'));
  for (const row of forecasts) assert.ok(Math.abs(predictDemand(row.date, row.baseline, model) - row.prediction) < 0.000051, row.date);
});
