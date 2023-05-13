

export function calculateString(str) {
  if(!str) return '';
  const numbers = str.split(/[-+]/).map(Number);
  const operators = str.replace(/[0-9]/g, '').split('');

  let result = numbers[0];

  for (let i = 0; i < operators.length; i++) {
    if (operators[i] === '+') {
      result += numbers[i + 1];
    } else if (operators[i] === '-') {
      result -= numbers[i + 1];
    }
  }
  return result;
}


