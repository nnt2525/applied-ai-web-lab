export function filterRows(rows, { month = 'all', category = 'all', channel = 'all' } = {}) {
  return rows.filter(row => (month === 'all' || row.date.startsWith(month)) && (category === 'all' || row.category === category) && (channel === 'all' || row.channel === channel));
}

export function summarize(rows) {
  const summary = rows.reduce((acc, row) => ({ revenue: acc.revenue + row.revenue, cost: acc.cost + row.cost, units: acc.units + row.units }), { revenue: 0, cost: 0, units: 0 });
  return { ...summary, profit: summary.revenue - summary.cost, margin: summary.revenue ? (summary.revenue - summary.cost) / summary.revenue : 0, records: rows.length };
}

export function groupRows(rows, key) {
  const grouped = new Map();
  for (const row of rows) {
    const group = grouped.get(row[key]) || { name: row[key], category: row.category, revenue: 0, cost: 0, units: 0 };
    group.revenue += row.revenue;
    group.cost += row.cost;
    group.units += row.units;
    grouped.set(row[key], group);
  }
  return [...grouped.values()];
}

export function toCSV(rows) {
  const columns = ['date', 'category', 'product', 'units', 'unit_price', 'revenue', 'cost', 'channel'];
  const escape = value => {
    let text = String(value ?? '');
    if (/^[=+\-@\t\r]/.test(text)) text = "'" + text;
    return /[",\r\n]/.test(text) ? `"${text.replaceAll('"', '""')}"` : text;
  };
  return [columns.join(','), ...rows.map(row => columns.map(column => escape(row[column])).join(','))].join('\r\n');
}
