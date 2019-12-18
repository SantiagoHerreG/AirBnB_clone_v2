#!/usr/bin/python3
"""test for state"""
import unittest
from unittest.mock import patch
from io import StringIO
import console
import tests
from console import HBNBCommand
import os
from models.state import State
from models.base_model import BaseModel, Base
import pep8
from models.engine.db_storage import DBStorage
import MySQLdb


class TestState(unittest.TestCase):
    """this will test the State class"""

    @classmethod
    def setUpClass(cls):
        """set up for test"""
        cls.state = State()
        cls.state.name = "CA"
        cls.consol = HBNBCommand()

    @classmethod
    def teardown(cls):
        """at the end of the test this will tear it down"""
        del cls.state
        del cls.consol

    def tearDown(self):
        """teardown"""
        try:
            os.remove("file.json")
        except Exception:
            pass

    def test_pep8_Review(self):
        """Tests pep8 style"""
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(['models/state.py'])
        self.assertEqual(p.total_errors, 0, "fix pep8")

    def test_checking_for_docstring_State(self):
        """checking for docstrings"""
        self.assertIsNotNone(State.__doc__)

    def test_attributes_State(self):
        """chekcing if State have attributes"""
        self.assertTrue('id' in self.state.__dict__)
        self.assertTrue('created_at' in self.state.__dict__)
        self.assertTrue('updated_at' in self.state.__dict__)
        self.assertTrue('name' in self.state.__dict__)

    def test_is_subclass_State(self):
        """test if State is subclass of BaseModel"""
        self.assertTrue(issubclass(self.state.__class__, BaseModel), True)

    def test_attribute_types_State(self):
        """test attribute type for State"""
        self.assertEqual(type(self.state.name), str)

    def test_save_State(self):
        """test if the save works"""
        self.state.save()
        self.assertNotEqual(self.state.created_at, self.state.updated_at)

    def test_to_dict_State(self):
        """test if dictionary works"""
        self.assertEqual('to_dict' in dir(self.state), True)

    @unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") != "db", "Useless in fs")
    def test_create_state_in_db(self):
        """Test for method delete when using database
        """
        db_conn = MySQLdb.connect(host=os.getenv("HBNB_MYSQL_HOST"),
                                  port=3306,
                                  user=os.getenv("HBNB_MYSQL_USER"),
                                  passwd=os.getenv("HBNB_MYSQL_PWD"),
                                  db=os.getenv("HBNB_MYSQL_DB"),
                                  charset="utf8")

        curs = db_conn.cursor()
        curs.execute("SELECT COUNT(*) FROM states")
        query_res = curs.fetchone()
        if len(query_res):
            n_obj = query_res[0]
        else:
            n_obj = 0
        curs.close()
        db_conn.close()
        db_conn2 = MySQLdb.connect(host=os.getenv("HBNB_MYSQL_HOST"),
                                   port=3306,
                                   user=os.getenv("HBNB_MYSQL_USER"),
                                   passwd=os.getenv("HBNB_MYSQL_PWD"),
                                   db=os.getenv("HBNB_MYSQL_DB"),
                                   charset="utf8")
        self.consol.onecmd("create State name=\"Texas\"")
        curs = db_conn2.cursor()
        curs.execute("SELECT COUNT(*) FROM states")
        query_res = curs.fetchone()
        if len(query_res):
            new_obj = query_res[0]
        else:
            new_obj = 0
        curs.close()
        db_conn2.close()
        self.assertTrue(new_obj - n_obj == 1)

if __name__ == "__main__":
    unittest.main()
