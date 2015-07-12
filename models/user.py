from models.json_model import JsonModel
from bson import ObjectId
__author__ = 'barryhobbs'

class User(JsonModel):
    def __init__(self, _id=None, name=None):
        if not name:
            raise ValueError("name is required for User")
        self._id = _id
        self.name = name

    def __str__(self):
        return "<User: _id=%s, name=%s>" % (self._id, self.name)

    def to_json(self):
        return {"_id": str(self._id), "name": self.name}

    def to_motor_create_json(self):
        return {"name": self.name}

    @classmethod
    def from_db_rep(cls, db_rep):
        return cls(_id=ObjectId(db_rep['_id']), name=db_rep['name'])
