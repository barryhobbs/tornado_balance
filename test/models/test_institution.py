from unittest import TestCase
from models.institution import Institution

__author__ = 'barryhobbs'


class TestInstitution(TestCase):

    def test_basic_institution_constructor(self):
        institution = Institution(name="Test Bank", type=Institution.TYPES[0])
        self.assertEqual(institution.name, "Test Bank")
        self.assertEqual(institution.type, Institution.TYPES[0])

    def test_institution_constructor_requirements(self):
        with self.assertRaises(ValueError):
            Institution()

        with self.assertRaises(ValueError):
            Institution(name="Test Bank", type=None)

        with self.assertRaises(ValueError):
            Institution(type=Institution.TYPES[0])

        with self.assertRaises(ValueError):
            Institution(name="Test Bank", type="Bad Type")

    def test_institution_str(self):
        institution = Institution(_id=1, name="Test Bank", type=Institution.TYPES[1], user_id=1)
        self.assertEqual(
            "<Institution: _id=1, name=Test Bank, type=SAVING, user_id=1>", str(institution))

    def test_institution_to_json(self):
        institution = Institution(_id=1, name="Test Bank", type=Institution.TYPES[1], user_id=1)
        self.assertEqual({"_id": "1", "name": "Test Bank", "type": Institution.TYPES[1], "user_id": 1},
                         institution.to_json())

    def test_institution_repr(self):
        institution = Institution(_id=1, name="Test Bank", type=Institution.TYPES[1], user_id=1)
        self.assertEqual('{"user_id": 1, "_id": "1", "type": "SAVING", "name": "Test Bank"}', repr(institution))