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


@app.route('/python/', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def show_python(text="is_cool"):
    """Handles a request to route /python/(<text>)
    """
    return "Python {}".format(text.replace("_", " "))


@app.route('/number/<int:n>', strict_slashes=False)
def show_number(n):
    """Handles a request to route /number/n where n is an integer
    """
    return "{} is a number".format(n)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
