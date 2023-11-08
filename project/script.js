function checkGuess() {
    let random_number = Math.floor(Math.random() * 100) + 1;
    let attempts = 0;
    let userInput = document.getElementById('userInput').value;
    let result = document.getElementById('result');

    if (userInput === '') {
        result.innerText = 'Please enter a number.';
    } else {
        let guess = parseInt(userInput);
        attempts++;

        if (isNaN(guess)) {
            result.innerText = 'Invalid input. Please enter a valid number.';
        } else if (guess === random_number) {
            result.innerText = `Congratulations! You guessed the number in ${attempts} attempts!`;
        } else if (guess < random_number) {
            result.innerText = 'Try a higher number.';
        } else {
            result.innerText = 'Try a lower number.';
        }
    }
}
