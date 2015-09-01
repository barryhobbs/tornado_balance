import logging
import tornado
from handlers.json_web_request_handler import JsonWebRequestHandler
from models.institution import Institution

__author__ = 'barryhobbs'
logger = logging.getLogger("balance")

class InstitutionHandler(JsonWebRequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, args=None):
        logger.debug("--json=%s-- %s\n%s\n%s" % (self.produce_json, self.request.headers, self.request.body, args))
        db = self.settings['db']
        cursor = db.institutions.find()
        institutions = []
        while (yield cursor.fetch_next):
            document = cursor.next_object()
            inst = Institution.from_db_rep(document)
            dict=inst.to_json()
            user = yield db.users.find_one(id)  # This doesn't work.  I think I need to make it all in one doc. Yay nosql
            dict['user_name'] = user['name']
            institutions.append(dict)
        if self.produce_json:
            self.write(dict(result=institutions))
        else:
            self.render("templ_institution.html")

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        logger.debug("------ %s\n%s" % (self.request.headers, self.request.body))
        params = self.json_args
        name = None
        type = Institution.TYPES[3]
        user_id = None

        for field in params:
            logger.info("Field = %s" % field)
            if field[u'name'] == u'name':
                name = field[u'value']
            if field[u'name'] == u'type':
                type = field[u'value']
            if field[u'name'] == u'user_id':
                user_id = field[u'value']

        institution = Institution(name=name, type=type, user_id=user_id)
        logger.debug(">>>>>>>>> %s" % institution)
        db = self.settings['db']
        result = yield db.institutions.insert(institution.to_motor_create_json())
        logger.debug("XXXXXXXX result = %s" % result)
        self.finish()
