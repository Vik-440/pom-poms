export function formatNumber(number: string | number) {
  const opts = { minimumFractionDigits: 0, style: 'currency', };
  return number.toLocaleString('de-CH');
}