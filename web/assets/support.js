import { classify } from './inference.js';

const names = { account: 'Account access', billing: 'Billing', delivery: 'Delivery', technical: 'Technical support' };
const descriptions = { account: 'Login, password, profile, and account access.', billing: 'Payments, refunds, invoices, and billing questions.', delivery: 'Shipping, tracking, and delivery questions.', technical: 'Application errors, performance, and technical problems.' };
const form = document.querySelector('#classify-form');
const input = document.querySelector('#message');
const button = document.querySelector('#classify-button');
const output = document.querySelector('#prediction');
let model;
const percent = value => `${(value * 100).toFixed(1)}%`;

function element(tag, className, text) {
  const el = document.createElement(tag);
  if (className) el.className = className;
  if (text !== undefined) el.textContent = text;
  return el;
}

function showPrediction() {
  if (!model || !input.reportValidity()) return;
  try {
    const started = performance.now();
    const result = classify(input.value, model);
    const elapsed = performance.now() - started;
    const content = document.createDocumentFragment();
    content.append(element('span', 'prediction-label', result.abstained ? 'MODEL ABSTAINED / REVIEW NEEDED' : 'PREDICTED QUEUE'));
    const heading = element('div', `prediction-heading${result.abstained ? ' abstained' : ''}`);
    heading.append(element('h3', '', result.abstained ? 'Needs a human look.' : names[result.label]), element('span', 'prediction-icon', result.abstained ? '?' : '↳'));
    content.append(heading, element('p', 'prediction-description', result.abstained ? `The highest-scoring queue was ${names[result.label]}. No automatic route is recommended.` : descriptions[result.label]));
    const distribution = element('div', 'score-distribution');
    for (const row of result.scores) {
      const line = element('div', 'score-row');
      const meta = element('div', 'score-meta');
      meta.append(element('span', '', names[row.label]), element('span', '', percent(row.score)));
      const track = element('div', 'score-track');
      const fill = element('div', 'score-fill');
      fill.style.width = `${row.score * 100}%`;
      track.append(fill);
      line.append(meta, track);
      distribution.append(line);
    }
    content.append(element('span', 'tiny-label', 'UNCALIBRATED MODEL SCORE'), distribution);
    const meta = element('div', 'inference-meta');
    meta.append(element('span', '', `Pattern coverage ${percent(result.coverage)}`), element('span', '', `${elapsed.toFixed(1)} ms · this browser`));
    content.append(meta);
    content.append(element('p', 'prediction-warning', result.abstained ? result.reasons.join(' ') : 'A high score is not a guarantee. This model can confidently misclassify unfamiliar messages; review important decisions.'));
    output.replaceChildren(content);
  } catch (error) {
    output.replaceChildren(element('p', 'error-message', error.message));
  }
}

input.addEventListener('input', () => { document.querySelector('#char-count').textContent = `${input.value.length} / 1000`; });
form.addEventListener('submit', event => { event.preventDefault(); showPrediction(); });
document.querySelectorAll('[data-example]').forEach(sample => sample.addEventListener('click', () => {
  input.value = sample.dataset.example;
  input.dispatchEvent(new Event('input'));
  showPrediction();
}));

try {
  const responses = await Promise.all([fetch('assets/models/support-model.json'), fetch('assets/data/metrics.json')]);
  for (const response of responses) if (!response.ok) throw new Error('Model assets could not be loaded. Please serve this folder over HTTP.');
  const [loadedModel, metrics] = await Promise.all(responses.map(response => response.json()));
  model = loadedModel;
  button.disabled = false;
  document.querySelector('#model-status').textContent = '● Trained model · runs locally';
  const classifier = metrics.classifier;
  const cards = [
    ['Held-out macro F1', classifier.test.macro_f1.toFixed(2), `${classifier.test.n} authored test messages · four queues`],
    ['Majority baseline', percent(classifier.majority_baseline.accuracy), 'Baseline accuracy · compare with model card'],
    ['Unfamiliar text rejected', percent(classifier.unknown_test.rejection_rate), `${classifier.unknown_test.n} held-out outside-task examples · limited protection`],
    ['Training examples', String(classifier.split_counts.train), `${classifier.split_counts.dev} dev / ${classifier.split_counts.test} test · family-separated`]
  ];
  const evaluation = document.querySelector('#evaluation');
  evaluation.replaceChildren(...cards.map(([title, value, note]) => {
    const card = element('div', 'eval-card');
    card.append(element('span', '', title), element('strong', '', value), element('small', '', note));
    return card;
  }));
} catch (error) {
  document.querySelector('#model-status').textContent = '○ Model unavailable';
  output.replaceChildren(element('p', 'error-message', error.message));
  document.querySelector('#evaluation').textContent = 'Evaluation unavailable. Reload after checking the server.';
}
