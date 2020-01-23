#!/usr/bin/python3
"""Uses the Flask micro framework to make an app server listen at 0.0.0.0:5000
"""
from flask import render_template
from flask import Flask
from models import storage
from models import State
from models import Amenity
from models import Place
from models import User


app = Flask(__name__)


@app.teardown_appcontext
def teardown_context_custom(empty):
    """remove the current SQLAlchemy Session
    """
    storage.close()


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """display a HTML done during
    the project 0x01. AirBnB clone - Web static
    """
    list_amenities = []
    amenities = storage.all(Amenity)
    for key, value in amenities.items():
        list_amenities.append((value.__dict__["name"]))

    list_amenities.sort()

    states = storage.all(State)
    list_states = []
    for key, value in states.items():
        cities = []
        for city in value.cities:
            cities.append(city.__dict__["name"])
        cities.sort()
        tuple_state_and_cities = (cities, value.__dict__["name"])
        list_states.append(tuple_state_and_cities)

    places = storage.all(Place)
    list_places = []
    users = storage.all(User)
    for key, value in places.items():
        user_id = value.__dict__["user_id"]
        user = users["User." + user_id]
        user_name = user.first_name + " " + user.last_name
        list_places.append((value.__dict__["name"], value, user_name))

    list_places.sort()

    return render_template('100-hbnb.html',
                           var=(list_states, list_amenities, list_places))


if __name__ == '__main__':

    app.run(host='0.0.0.0', port='5000')
