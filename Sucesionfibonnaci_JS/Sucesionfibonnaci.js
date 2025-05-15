function fibonacciSequence(n) {
    const sequence = [];

    if (n <= 0) return sequence;

    sequence.push(0);
    if (n === 1) return sequence;

    sequence.push(1);
    for (let i = 2; i < n; i++) {
        sequence.push(sequence[i - 1] + sequence[i - 2]);
    }

    return sequence;
}

// Pedir al usuario el número de términos (solo funciona en entorno Node.js)
const readline = require('readline').createInterface({
    input: process.stdin,
    output: process.stdout
});

readline.question('Enter the number of Fibonacci terms to generate: ', (input) => {
    const terms = parseInt(input);

    if (isNaN(terms) || terms < 0) {
        console.log('Please enter a valid non-negative integer.');
    } else {
        const sequence = fibonacciSequence(terms);
        console.log('Fibonacci sequence:');
        console.log(sequence.join(' '));
    }

    readline.close();
});
