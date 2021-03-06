from decimal import *
import datetime
import json
import logging
from bson import ObjectId
from models.constants import Constants

__author__ = 'barryhobbs'
logger = logging.getLogger("balance")


class AccountBalance:
    def __init__(self, _id=None, institution=None, balance=None, pennies=None, last_update=None):
        logger.info("(institution = %s, balance = %s, last_update = %s" % (institution, balance, last_update))
        if not institution or not (balance or pennies):
            raise ValueError("institution and (balance or pennies) are required")
        self._id = _id
        self.institution = institution
        if pennies:
            self.balance = pennies
        else:
            decimal = Decimal(balance)
            with localcontext(BasicContext):
                pennies = decimal * 100
                pennies = pennies.to_integral_value()
                self.balance = int(pennies)
        logger.debug("pennies? = %s" % self.balance)
        self.last_update = last_update

    def __str__(self):
        return "<AccountBalance: id=%s, institution=%s, balance=%s, last_update=%s>" % (
            str(self._id), self.institution, self.get_balance_string(),
            self.last_update.strftime(Constants.TIME_FORMAT))

    def __repr__(self):
        return json.dumps(self.to_json())

    def to_json(self):
        return {"_id": str(self._id), "institution": self.institution, "balance": self.balance,
                "last_update": self.last_update.strftime(Constants.TIME_FORMAT),
                "formatted_balance": self.get_balance_string()}

    def to_motor_create_json(self):
        return {"institution": self.institution, "balance": self.balance,
                "last_update": self.last_update.strftime(Constants.TIME_FORMAT)}

    def get_balance_string(self):
        return '{:,.2f}'.format((Decimal(self.balance) / 100))

    @classmethod
    def from_db_rep(cls, db_rep):
        return cls(_id=ObjectId(db_rep['_id']), institution=db_rep['institution'], pennies=db_rep['balance'],
                   last_update=datetime.datetime.strptime(db_rep['last_update'], Constants.TIME_FORMAT))
