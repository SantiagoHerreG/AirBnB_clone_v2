#!/usr/bin/python3
"""This is the place class"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy import Table
from sqlalchemy.orm import relationship
from models.review import Review

metadata = Base.metadata
place_amenity = Table('place_amenity', metadata,
                      Column('place_id', String(60), ForeignKey('places.id'),
                             primary_key=True, nullable=False),
                      Column('amenity_id', String(60), ForeignKey('ameni\
ties.id'),
                             primary_key=True, nullable=False))


class Place(BaseModel, Base):
    """This is the class for Place
    Attributes:
        city_id: city id
        user_id: user id
        name: name input
        description: string of description
        number_rooms: number of room in int
        number_bathrooms: number of bathrooms in int
        max_guest: maximum guest in int
        price_by_night:: pice for a staying in int
        latitude: latitude in flaot
        longitude: longitude in float
        amenity_ids: list of Amenity ids
    """
    __tablename__ = "places"

    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []

    reviews = relationship("Review", cascade="all,delete", backref="place")
    amenities = relationship("Amenity",
                             secondary=place_amenity,
                             viewonly=False,
                             backref="place_amenities")

    @property
    def reviews(self):
        """returns the list of Review instances with place_id
        equals to the current Place.id
        """
        reviews_dict = models.storage.all(Review)
        new_dict = {}
        for key, value in reviews_dict.items():
            if self.id == value.place_id:
                new_dict[key] = value
        return new_dict

    @property
    def amenities(self):
        """Getter of all amenities contained in the database
        """
        return self.amenity_ids

    @amenities.setter
    def amenities(self, obj):
        """Handles new append method for saving amenities ids
        """
        if type(obj) == Amenity:
            self.append(obj)

        def append(self, obj):
            """Method that appends
            """
            self.amenity_ids.append(obj)
