from bson import ObjectId
from models.json_model import JsonModel
__author__ = 'barryhobbs'

class Institution(JsonModel):
    TYPES=['CHECKING', 'SAVING', 'CREDIT', 'UNTRACKED']
    def __init__(self, _id=None, name=None, type='UNTRACKED', user_id=None):
        if not name or not type or type not in Institution.TYPES:
            raise ValueError("name and type are required for Institution, and type must be one of %s" %
                             Institution.TYPES)
        self._id = _id
        self.name = name
        self.type = type
        self.user_id = user_id

    def __str__(self):
        return "<Institution: _id=%s, name=%s, type=%s, user_id=%s>" % (
            str(self._id), self.name, self.type, self.user_id)

    def to_json(self):
        return {"_id": str(self._id), "name": self.name, "type": self.type, "user_id": self.user_id}

    def to_motor_create_json(self):
        return {"name": self.name, "type": self.type, "user_id": self.user_id}

    @classmethod
    def from_db_rep(cls, db_rep):
        return cls(_id=ObjectId(db_rep['_id']), name=db_rep['name'], type=db_rep['type'], user_id=db_rep['user_id'])
