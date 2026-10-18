import { filterRows, summarize, groupRows, toCSV } from './analysis.js';
import './forecast.js';
const money = number => new Intl.NumberFormat('en-US', { style: 'currency', currency: 'THB', currencyDisplay: 'narrowSymbol', maximumFractionDigits: 0 }).format(number);
const integer = number => new Intl.NumberFormat('en-US').format(number);
const percent = number => `${(number * 100).toFixed(1)}%`;
const filters = document.querySelector('#filters');
const status = document.querySelector('#dashboard-status');
let rows = [];
let selected = [];

function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}
function svgElement(tag, attributes, text) {
  const node = document.createElementNS('http://www.w3.org/2000/svg', tag);
  Object.entries(attributes).forEach(([key, value]) => node.setAttribute(key, value));
  if (text !== undefined) node.textContent = text;
  return node;
}
function drawRevenueChart(selectedRows) {
  const target = document.querySelector('#revenue-chart');
  const days = groupRows(selectedRows, 'date').sort((a, b) => a.name.localeCompare(b.name));
  if (!days.length) { target.replaceChildren(el('p', 'empty-data', 'No data for this selection.')); return; }
  const width = 600, height = 230, left = 52, right = 12, top = 18, bottom = 37;
  const chartWidth = width - left - right, chartHeight = height - top - bottom;
  const max = Math.max(...days.map(day => day.revenue)) * 1.12 || 1;
  const x = index => left + (days.length > 1 ? index / (days.length - 1) : .5) * chartWidth;
  const y = value => top + chartHeight * (1 - value / max);
  const chart = svgElement('svg', { viewBox: `0 0 ${width} ${height}`, role: 'img', 'aria-label': `Daily revenue across ${days.length} dates. Total ${money(summarize(selectedRows).revenue)}.` });
  for (let tick = 0; tick <= 4; tick++) {
    const value = max * tick / 4;
    chart.append(svgElement('line', { x1: left, y1: y(value), x2: width - right, y2: y(value), stroke: '#edf1f7', 'stroke-dasharray': '3 4' }));
    chart.append(svgElement('text', { x: left - 10, y: y(value) + 3, 'text-anchor': 'end', class: 'chart-label' }, value >= 1000 ? `${Math.round(value / 1000)}k` : String(Math.round(value))));
  }
  const points = days.map((day, index) => `${x(index)},${y(day.revenue)}`).join(' ');
  chart.append(svgElement('polygon', { points: `${x(0)},${y(0)} ${points} ${x(days.length - 1)},${y(0)}`, fill: '#edf3ff' }));
  chart.append(svgElement('polyline', { points, fill: 'none', stroke: '#4e83ed', 'stroke-width': '2', 'stroke-linejoin': 'round' }));
  const labelIndices = [...new Set([0, Math.floor((days.length - 1) / 2), days.length - 1])];
  for (const index of labelIndices) {
    const date = new Date(days[index].name + 'T12:00:00Z').toLocaleDateString('en-US', { day: 'numeric', month: 'short', timeZone: 'UTC' });
    chart.append(svgElement('text', { x: x(index), y: height - 10, 'text-anchor': 'middle', class: 'chart-label' }, date));
  }
  target.replaceChildren(chart);
}

function render() {
  selected = filterRows(rows, { month: document.querySelector('#month-filter').value, category: document.querySelector('#category-filter').value, channel: document.querySelector('#channel-filter').value });
  const summary = summarize(selected);
  const cards = [['Total revenue', money(summary.revenue), 'Sum of selected sales'], ['Gross profit', money(summary.profit), 'Revenue minus product cost'], ['Gross margin', percent(summary.margin), 'Gross profit ÷ revenue'], ['Units sold', integer(summary.units), `${integer(summary.records)} daily aggregate records`]];
  document.querySelector('#kpis').replaceChildren(...cards.map(([title, value, note]) => {
    const card = el('div', 'kpi-card');
    card.append(el('span', '', title), el('strong', '', value), el('small', '', note)); return card;
  }));
  drawRevenueChart(selected);
  const categories = groupRows(selected, 'category').sort((a, b) => b.revenue - a.revenue);
  const categoryNodes = categories.map(category => {
    const row = el('div', 'category-row');
    const meta = el('div', 'score-meta');
    const share = summary.revenue ? category.revenue / summary.revenue : 0;
    meta.append(el('span', '', category.name), el('span', '', percent(share)));
    const track = el('div', 'score-track'), fill = el('div', 'score-fill');
    fill.style.width = `${share * 100}%`; track.append(fill); row.append(meta, track); return row;
  });
  document.querySelector('#category-chart').replaceChildren(...(categoryNodes.length ? categoryNodes : [el('p', 'empty-data', 'No matching categories.')]));
  const products = groupRows(selected, 'product').sort((a, b) => b.revenue - a.revenue);
  document.querySelector('#product-count').textContent = `${products.length} products`;
  document.querySelector('#product-table').replaceChildren(...products.map(product => {
    const row = el('tr');
    const categoryCell = el('td'); categoryCell.append(el('span', 'category-pill', product.category));
    row.append(el('td', '', product.name), categoryCell, el('td', '', integer(product.units)), el('td', '', money(product.revenue)), el('td', '', percent(product.revenue ? (product.revenue - product.cost) / product.revenue : 0)));
    return row;
  }));
  status.textContent = `${integer(selected.length)} selected records · ${new Set(selected.map(row => row.date)).size} days · currency THB · synthetic data`;
  document.querySelector('#export-button').disabled = !selected.length;
}

filters.addEventListener('change', render);
filters.addEventListener('reset', () => { setTimeout(render, 0); });
document.querySelector('#export-button').addEventListener('click', () => {
  const blob = new Blob(['\uFEFF' + toCSV(selected)], { type: 'text/csv;charset=utf-8' });
  const href = URL.createObjectURL(blob), link = el('a');
  link.href = href; link.download = 'fieldnotes-synthetic-sales.csv'; document.body.append(link); link.click(); link.remove(); setTimeout(() => URL.revokeObjectURL(href), 1000);
});

try {
  const response = await fetch('assets/data/sales.json');
  if (!response.ok) throw new Error('Could not load the dataset. Please check the local server.');
  rows = await response.json();
  for (const [selector, key] of [['#month-filter', 'date'], ['#category-filter', 'category'], ['#channel-filter', 'channel']]) {
    const options = [...new Set(rows.map(row => key === 'date' ? row.date.slice(0, 7) : row[key]))].sort();
    const select = document.querySelector(selector);
    for (const value of options) {
      const label = key === 'date' ? new Date(value + '-01T12:00:00Z').toLocaleDateString('en-US', { month: 'long', year: 'numeric', timeZone: 'UTC' }) : value;
      select.append(new Option(label, value));
    }
  }
  render();
} catch (error) {
  status.textContent = error.message;
  status.setAttribute('role', 'alert');
}
