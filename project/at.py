import random
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Set the range for the random number
lower_limit = 1
upper_limit = 100

# Generate a random number
random_number = random.randint(lower_limit, upper_limit)
attempts = 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_guess', methods=['POST'])
def check_guess():
    global attempts
    attempts += 1
    guess = int(request.form['guess'])

    if guess == random_number:
        return jsonify({'message': f'Congratulations! You guessed the number in {attempts} attempts!'})
    elif guess < random_number:
        return jsonify({'message': 'Try a higher number.'})
    else:
        return jsonify({'message': 'Try a lower number.'})

if __name__ == '__main__':
    app.run(debug=True)
