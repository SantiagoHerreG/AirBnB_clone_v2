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


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states_list():
    """Handles a request to /cities_by_state
    """
    list_states_and_cities = []
    states = storage.all(State)
    for key, value in states.items():
        cities = []
        for city in value.cities:
            cities.append((city.__dict__["name"], city.__dict__["id"]))
        cities.sort()
        list_states_and_cities.append((value.__dict__["name"],
                                       value.__dict__["id"], cities))

    list_states_and_cities.sort()
    return render_template('8-cities_by_states.html',
                           states=list_states_and_cities)


if __name__ == '__main__':

    app.run(host='0.0.0.0', port='5000')
