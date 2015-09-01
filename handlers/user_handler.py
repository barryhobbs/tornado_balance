import logging
import tornado
from handlers.json_web_request_handler import JsonWebRequestHandler
from models.user import User

__author__ = 'barryhobbs'
logger = logging.getLogger("balance")

class UserHandler(JsonWebRequestHandler):

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, args=None):
        logger.debug("--json=%s-- %s\n%s\nargs=%s" % (self.produce_json, self.request.headers, self.request.body, args))
        logger.debug("--request_args" % (self.request.args))
        db = self.settings['db']
        cursor = db.users.find()
        users = []
        while (yield cursor.fetch_next):
            document = cursor.next_object()
            users.append(User.from_db_rep(document).to_json())
        if self.produce_json:
            self.write(dict(result=users))
        else:
            self.render("templ_user.html")

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        logger.debug("------ %s\n%s" % (self.request.headers, self.request.body))
        params = self.json_args
        name = None
        for field in params:
            logger.info("Field = %s" % field)
            if field[u'name'] == u'name':
                name = field[u'value']

        user = User(name=name)
        logger.debug(">>>>>>>>> %s" % user)
        db = self.settings['db']
        result = yield db.users.insert(user.to_motor_create_json())
        logger.debug("XXXXXXXX result = %s" % result)
        self.finish()
