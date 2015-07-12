import json
import tornado
import logging

__author__ = 'barryhobbs'

logger = logging.getLogger("json_requests")

class JsonWebRequestHandler(tornado.web.RequestHandler):
    def prepare(self):
        content_type = self.request.headers.get("Content-Type")
        if content_type and content_type.startswith("application/json"):
            if not self.request.body:
                self.json_args = json.loads('[]')
            else:
                try:
                    self.json_args = json.loads(self.request.body)
                except ValueError:
                    self.json_args = json.loads('[]')
                    logger.warn("Did not find a json body in %s" % self.request.body)
            self.produce_json = True
        else:
            self.json_args = None
            self.produce_json = False
