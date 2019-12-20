#!/usr/bin/python3
"""test for db storage"""
import unittest
import pep8
import json
import os
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models import storage
from models.engine.db_storage import DBStorage


class TestDBStorage(unittest.TestCase):
    '''this will test the DBStorage'''

    @classmethod
    def setUpClass(cls):
        """set up for test"""
        cls.state = State()
        cls.state.id = 1234553
        cls.state.name = "California"
        if os.getenv("HBNB_TYPE_STORAGE") != "db":
            raise unittest.SkipTest("Useless in fs")

    def test_pep8_FileStorage(self):
        """Tests pep8 style"""
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(['models/engine/file_storage.py'])
        self.assertEqual(p.total_errors, 0, "fix pep8")

    def test_all(self):
        """tests if all works in File Storage"""
        obj = storage.all()
        self.assertIsNotNone(obj)
        self.assertEqual(type(obj), dict)

    def test_all_by_class(self):
        """Tests that it returns the list of objects of one type of class
        """
        storage.new(self.state)
        storage.save()
        key = type(self.state).__name__ + "." + str(self.state.id)
        obj = storage.all("State")
        self.assertTrue(key in obj.keys())
        self.assertTrue(type(obj[key]) is State)

    def test_new(self):
        """test when new is created"""
        user = User()
        user.id = 12345588
        user.name = "Kevin"
        user.email = "1234@yahoo.com"
        user.password = "hi"
        storage.new(user)
        user.save()
        obj = storage.all()
        key = type(user).__name__ + "." + str(user.id)
        self.assertIsNotNone(obj[key])

    def test_reload_dbstorage(self):
        """
        tests reload
        """
        session1 = storage._DBStorage__session
        storage.reload()
        session2 = storage._DBStorage__session
        self.assertTrue(session1 is not session2)
