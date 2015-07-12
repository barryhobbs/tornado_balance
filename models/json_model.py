import json
__author__ = 'barryhobbs'

class JsonModel:
    def __repr__(self):
        return json.dumps(self.to_json())

    def to_json(self):
        return json.dumps({"supported": False})