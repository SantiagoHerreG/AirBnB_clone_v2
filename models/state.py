#!/usr/bin/python3
"""This is the state class"""
from models.base_model import BaseModel, Base
from models.city import City
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """This is the class for State
    Attributes:
        name: input name
    """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship(City, cascade="all,delete", backref="state")

    @property
    def cities(self):
        """returns the list of City instances with state_id
        equals to the current State.id
        """
        cities_dict = models.storage.all(City)
        my_dict = {}
        for key, value in cities_dict.items():
            if value.id == self.id:
                my_dict[key] = value
        return my_dict
