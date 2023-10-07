function generateRandomMathProblem() {
    const num1 = Math.floor(Math.random() * 10) + 1; // Random number between 1 and 10
    const num2 = Math.floor(Math.random() * 10) + 1; // Random number between 1 and 10
    const answer = num1 + num2;

    console.log(num1 + " + " + num2);
    return answer;
}

for (let i = 0; i < 11; i++) {
    const answer = generateRandomMathProblem();
    console.log(answer);
}
