#!/usr/bin/python3
"""Uses the Flask micro framework to make an app server listen at 0.0.0.0:5000
"""
from flask import render_template
from flask import Flask
from models import storage
from models import State


app = Flask(__name__)


@app.teardown_appcontext
def teardown_context_custom(empty):
    """remove the current SQLAlchemy Session
    """
    storage.close()


@app.route('/states', strict_slashes=False)
def states():
    """Handles /states request for all the States
    """
    list_states = []
    states = storage.all(State)
    for key, value in states.items():
        list_states.append((value.__dict__["name"], value.__dict__["id"]))

    list_states.sort()
    return render_template('9-states.html', states=(list_states, None))


@app.route('/states/<id>', strict_slashes=False)
def cities_by_states_listid(id):
    """Handles a request to /cities_by_state
    """
    tuple_states_and_cities = ()
    states = storage.all(State)

    for key, value in states.items():
        if value.__dict__["id"] == id:
            cities = []
            for city in value.cities:
                cities.append((city.__dict__["name"], city.__dict__["id"]))
            cities.sort()
            tuple_states_and_cities = (cities, value.__dict__["name"])

    if len(tuple_states_and_cities) == 0:
        return render_template('9-states.html',
                               states=(None, None))

    return render_template('9-states.html',
                           states=tuple_states_and_cities)


if __name__ == '__main__':

    app.run(host='0.0.0.0', port='5000')
