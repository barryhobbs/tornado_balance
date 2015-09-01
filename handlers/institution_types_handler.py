import logging
import tornado
from handlers.json_web_request_handler import JsonWebRequestHandler
from models.institution import Institution

__author__ = 'barryhobbs'
logger = logging.getLogger("balance")

class InstitutionTypesHandler(JsonWebRequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, args=None):
        logger.debug("--json=%s-- %s\n%s\n%s" % (self.produce_json, self.request.headers, self.request.body, args))
        if self.produce_json:
            self.write(dict(result=Institution.TYPES))
