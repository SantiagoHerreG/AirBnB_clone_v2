#!/usr/bin/python3
"""Uses the Flask micro framework to make an app server listen at 0.0.0.0:5000
"""
from flask import render_template
from flask import Flask
from models import storage
from models import State

app = Flask(__name__)


@app.teardown_appcontext
def teardown_context_custom(a=None):
    """remove the current SQLAlchemy Session
    """
    storage.close()


@app.route('/states_list', strict_slashes=False)
def states_list():
    """Handles a request to /states_list
    """
    list_states = []
    states = storage.all(State)
    for key, value in states.items():
        list_states.append((value.__dict__["name"], value.__dict__["id"]))

    list_states.sort()
    
    return render_template('7-states_list.html', states=list_states)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
