#!/usr/bin/python3
"""Uses the Flask micro framework to make an app server listen at 0.0.0.0:5000
"""
from flask import render_template
from flask import Flask
from models import storage
from models import State
from models import Amenity


app = Flask(__name__)


@app.teardown_appcontext
def teardown_context_custom(empty):
    """remove the current SQLAlchemy Session
    """
    storage.close()


@app.route('/hbnb_filters', strict_slashes=False)
def filters():
    """display a HTML page like 6-index.html, which was done during
    the project 0x01. AirBnB clone - Web static
    """

    list_amenities = []
    amenities = storage.all(Amenity)
    for key, value in amenities.items():
        list_amenities.append((value.__dict__["name"]))

    list_amenities.sort()
    tuple_states_and_cities = ()
    states = storage.all(State)

    list_states = []
    for key, value in states.items():
        cities = []
        for city in value.cities:
            cities.append(city.__dict__["name"])
        cities.sort()
        tuple_state_and_cities = (cities, value.__dict__["name"])
        list_states.append(tuple_state_and_cities)

    return render_template('10-hbnb_filters.html',
                           var=(list_states, list_amenities))


if __name__ == '__main__':

    app.run(host='0.0.0.0', port='5000')
