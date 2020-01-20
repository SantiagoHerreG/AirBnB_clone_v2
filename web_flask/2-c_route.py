#!/usr/bin/python3
"""Uses the Flask micro framework to make an app server listen at 0.0.0.0:5000
"""
from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def home():
    """Function for handling the route /
    """
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """Handles /hbnb route
    """
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def show_text(text=None):
    """Handles a request to route /c/<text>
    """
    for letter in text:
        if letter == "_":
            letter = " "
    return "C {}".format(text)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
