import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { classify, normalizeText } from '../web/assets/inference.js';
const model = JSON.parse(await readFile(new URL('../web/assets/models/support-model.json', import.meta.url), 'utf8'));
const fixtures = JSON.parse(await readFile(new URL('./inference-fixtures.json', import.meta.url), 'utf8'));

test('browser model scores match exported Python inference fixtures', () => {
  for (const fixture of fixtures) {
    const result = classify(fixture.text, model);
    assert.equal(result.label, fixture.top_class, fixture.text);
    assert.equal(result.abstained, fixture.abstained, fixture.text);
    assert.ok(Math.abs(result.coverage - fixture.coverage) < 1e-10, fixture.text);
    for (const row of result.scores) assert.ok(Math.abs(row.score - fixture.posterior[row.label]) < 1e-10, fixture.text);
  }
});
test('blank and excessive inputs are rejected before inference', () => {
  assert.throws(() => classify('   ', model), /add a message/);
  assert.throws(() => classify('a'.repeat(1001), model), /at most/);
});
test('unseen patterns abstain with finite normalized scores', () => {
  const result = classify('🦄🦄🦄🦄🦄', model);
  assert.equal(result.abstained, true);
  assert.equal(result.coverage, 0);
  assert.ok(Math.abs(result.scores.reduce((sum, row) => sum + row.score, 0) - 1) < 1e-12);
});
test('NFKC, case and whitespace normalization supports fullwidth text', () => {
  assert.equal(normalizeText('  ＰＡＹＭＥＮＴ\n\t refund  '), 'payment refund');
});
