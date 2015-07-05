from unittest import TestCase
import datetime
from models.account_balance import AccountBalance
from models.constants import Constants

__author__ = 'barryhobbs'


class TestAccountBalance(TestCase):
    def setUp(self):
        self.now = datetime.datetime.strptime("2002/12/31,23:59:59", Constants.TIME_FORMAT)

    def test_account_balance_constructor(self):
        ab = AccountBalance(institution="Test Bank", balance=500.59, last_update=self.now)
        self.assertEqual(ab.institution, "Test Bank")
        self.assertEqual(ab.balance, 50059)
        self.assertEqual(ab.last_update, self.now)
        self.assertEqual("500.59", ab.get_balance_string())

        ab = AccountBalance(institution="Test Bank", balance=1500, last_update=self.now)
        self.assertEqual(150000, ab.balance)

        ab = AccountBalance(institution="Test Bank", pennies=150045, last_update=self.now)
        self.assertEqual(150045, ab.balance)

    def test_account_balance_balance_string(self):
        ab = AccountBalance(institution="Test Bank", balance=1500.59, last_update=self.now)
        self.assertEqual("1,500.59", ab.get_balance_string())

    def test_account_balance_str(self):
        ab = AccountBalance(institution="Test Bank", balance=1500.59, last_update=self.now)
        ab._id = 1
        self.assertEqual(
            "<AccountBalance: id=1, institution=Test Bank, balance=1,500.59, last_update=2002/12/31,23:59:59>", str(ab))
