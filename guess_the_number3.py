# Zgadnij liczbę 3. Framework Flask

from random import randint
from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def guess_number():
    """
    Handles GET and POST requests for the main page of the game. Renders the HTML template
    for the page, which includes an input form for the user to make guesses and buttons
    to submit their guesses or start a new game.

    For POST requests, checks the user's guess against the secret number and updates the range
    of possible numbers based on whether the guess was too high or too low. If the user guessed
    correctly, returns a message indicating they won.

    Returns:
        str: HTML template for the game page
    """

    # Check if the user has submitted a guess
    if request.method == 'POST':
        # Get the minimum and maximum values of the range
        min_value = int(request.form['min_value'])
        max_value = int(request.form['max_value'])

        # Check if the user has made a guess
        if 'number' in request.form:
            number = int(request.form['number'])
            if 'too_small' in request.form:
                # If the guess was too low, update the minimum value of the range
                # and generate a new secret number within the updated range
                min_value = number + 1
                number = randint(min_value, max_value)
            elif 'too_big' in request.form:
                # If the guess was too high, update the maximum value of the range
                # and generate a new secret number within the updated range
                max_value = number - 1
                number = randint(min_value, max_value)
        else:
            # If the user has not yet made a guess, generate a new secret number within the
            # default range of 0 to 100
            number = randint(min_value, max_value)

        if 'you_win' in request.form:
            # If the user has correctly guessed the secret number, return a message indicating
            # they won
            return 'Computer win!'

    else:
        # If this is a GET request (i.e. the user is loading the page for the first time),
        # set the default range of 0 to 100 and don't set a secret number yet
        min_value = 0
        max_value = 100
        number = None

    # Render the HTML template for the game page, passing in the range and current guess
    return render_template('guess.html', min_value=min_value, max_value=max_value, number=number)


if __name__ == '__main__':
    app.run(debug=True)
