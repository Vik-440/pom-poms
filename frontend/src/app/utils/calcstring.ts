function add(a, b) {
  return a + b;
}

function subtract(a, b) {
  return a - b;
}

function multiply(a, b) {
  return a * b;
}

function divide(a, b) {
  return a / b;
}

export function calculateString(expression) {
  if(!expression) return '';
  const numbers = expression.match(/\d+/g).map(Number);
  const operators = expression.match(/[\+\-\*\/]/g);
  let result = numbers[0];
  if(!operators) {
    return expression;
  }
  
  for (let i = 0; i < operators.length; i++) {
    const operator = operators[i];
    const number = numbers[i + 1];
    
    switch (operator) {
      case '+':
        result = add(result, number);
        break;
      case '-':
        result = subtract(result, number);
        break;
      case '*':
        result = multiply(result, number);
        break;
      case '/':
        result = divide(result, number);
        break;
    }
  }
  
  return result;
}

