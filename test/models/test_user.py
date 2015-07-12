from unittest import TestCase
from models.user import User
__author__ = 'barryhobbs'

class TestUser(TestCase):
    def test_user_basic_constructor(self):
        user = User(name="Bob")
        self.assertEqual(user.name, "Bob")

    def test_user_constructor_requirements(self):
        with self.assertRaises(ValueError):
            User()

        with self.assertRaises(ValueError):
            User(_id="1")

        with self.assertRaises(ValueError):
            User(name=None)

    def test_user_str(self):
        user = User(_id="1", name="Bob")
        self.assertEqual("<User: _id=1, name=Bob>", str(user))

    def test_user_to_json(self):
        user = User(_id="1", name="Bob")
        self.assertEqual({"_id": "1", "name": "Bob"}, user.to_json())

    def test_user_repr(self):
        user = User(_id="1", name="Bob")
        self.assertEqual('{"_id": "1", "name": "Bob"}', repr(user))