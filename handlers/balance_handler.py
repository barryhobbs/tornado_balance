import datetime
import tornado
import logging
from handlers.json_web_request_handler import JsonWebRequestHandler

from models.account_balance import AccountBalance

__author__ = 'barryhobbs'
logger = logging.getLogger("balance")


class BalanceHandler(JsonWebRequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        logger.debug("--json=%s-- %s\n%s" % (self.produce_json, self.request.headers, self.request.body))
        db = self.settings['db']
        cursor = db.account_balances.find()
        balances = []
        while (yield cursor.fetch_next):
            document = cursor.next_object()
            balances.append(AccountBalance.from_db_rep(document).to_json())
        if self.produce_json:
            self.write(dict(result=balances))
        else:
            self.render("templ_balance.html")

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        logger.debug("------ %s\n%s" % (self.request.headers, self.request.body))
        params = self.json_args
        institution = None
        balance = None
        for field in params:
            logger.info("Field = %s" % field)
            if field[u'name'] == u'institution':
                institution = field[u'value']
            elif field[u'name'] == u'current_balance':
                balance = field[u'value']

        ab = AccountBalance(institution=institution, balance=balance, last_update=datetime.datetime.utcnow())
        logger.debug(">>>>>>>>> %s" % ab)
        db = self.settings['db']
        result = yield db.account_balances.insert(ab.to_motor_create_json())
        logger.debug("XXXXXXXX result = %s" % result)
        self.finish()
