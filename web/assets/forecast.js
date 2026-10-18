import { predictDemand } from './demand.js';

function svg(tag, attributes, text) {
  const node = document.createElementNS('http://www.w3.org/2000/svg', tag);
  Object.entries(attributes).forEach(([key, value]) => node.setAttribute(key, value));
  if (text !== undefined) node.textContent = text;
  return node;
}
function chart(rows) {
  const width = 590, height = 230, left = 35, right = 12, top = 18, bottom = 32;
  const max = Math.max(...rows.flatMap(row => [row.actual, row.prediction, row.baseline])) * 1.12;
  const x = index => left + index / (rows.length - 1) * (width - left - right);
  const y = value => top + (1 - value / max) * (height - top - bottom);
  const result = svg('svg', { viewBox: `0 0 ${width} ${height}`, role: 'img', 'aria-label': 'Actual, ridge model and last-week baseline units over 28 held-out September days.' });
  for (let tick = 0; tick <= 3; tick++) {
    const value = tick * max / 3;
    result.append(svg('line', { x1: left, x2: width - right, y1: y(value), y2: y(value), stroke: '#edf1f7' }));
    result.append(svg('text', { x: left - 8, y: y(value) + 4, class: 'chart-label', 'text-anchor': 'end' }, String(Math.round(value))));
  }
  for (const [key, color, dash] of [['baseline', '#b3becb', '5 4'], ['prediction', '#5c9371', ''], ['actual', '#4e83ed', '']]) {
    result.append(svg('polyline', { points: rows.map((row, index) => `${x(index)},${y(row[key])}`).join(' '), fill: 'none', stroke: color, 'stroke-width': 2, 'stroke-dasharray': dash }));
  }
  for (const index of [0, 13, 27]) result.append(svg('text', { x: x(index), y: height - 8, class: 'chart-label', 'text-anchor': 'middle' }, rows[index].date.slice(5)));
  document.querySelector('#forecast-chart').replaceChildren(result);
}

try {
  const urls = ['assets/models/demand-model.json', 'assets/data/forecast.json', 'assets/data/metrics.json'];
  const values = await Promise.all(urls.map(async url => {
    const response = await fetch(url); if (!response.ok) throw new Error('Demand model assets could not be loaded.'); return response.json();
  }));
  const [model, predictions, metrics] = values;
  chart(predictions.filter(row => row.split === 'test'));
  const info = document.querySelector('#forecast-metrics');
  for (const [label, value] of [['Model test MAE', metrics.forecast.test.mae], ['Last-week test MAE', metrics.forecast.last_week_baseline.mae]]) {
    const metric = document.createElement('p'), title = document.createElement('span'), number = document.createElement('strong');
    title.textContent = label; number.textContent = `${value.toFixed(2)} units`; metric.append(title, number); info.append(metric);
  }
  const form = document.querySelector('#forecast-form');
  const result = document.querySelector('#forecast-result');
  function predict() {
    if (!form.reportValidity()) return;
    try {
      const date = document.querySelector('#forecast-date').value;
      const value = predictDemand(date, Number(document.querySelector('#lag-units').value), model);
      result.replaceChildren();
      const label = document.createElement('span'), number = document.createElement('strong');
      label.textContent = `Model estimate · ${date}`; number.textContent = `${value.toFixed(1)} units`; result.append(label, number);
    } catch (error) { result.textContent = error.message; }
  }
  form.addEventListener('submit', event => { event.preventDefault(); predict(); });
  predict();
} catch (error) {
  document.querySelector('#forecast-result').textContent = error.message;
  document.querySelector('#forecast-form button').disabled = true;
}
