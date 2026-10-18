export function predictDemand(dateString, lagUnits, model) {
  const day = new Date(dateString + 'T00:00:00Z');
  if (!Number.isFinite(day.getTime()) || !Number.isFinite(lagUnits) || lagUnits < 0) throw new Error('Choose a valid date and nonnegative units.');
  const index = (day - new Date('2026-04-01T00:00:00Z')) / 86400000;
  const weekend = [0, 6].includes(day.getUTCDay()) ? 1 : 0;
  const features = [index, weekend, Math.sin(2 * Math.PI * index / 7), Math.cos(2 * Math.PI * index / 7), Math.sin(2 * Math.PI * index / 30), Math.cos(2 * Math.PI * index / 30), [9, 10, 25].includes(day.getUTCDate()) ? 1 : 0, lagUnits];
  return Math.max(model.clip_min, model.intercept + features.reduce((sum, value, index) => sum + model.coefficients[index] * (value - model.means[index]) / model.scales[index], 0));
}
