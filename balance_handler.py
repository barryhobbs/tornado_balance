import json
import datetime
import tornado
from tornado import gen

from models.account_balance import AccountBalance

__author__ = 'barryhobbs'


class BalanceHandler(tornado.web.RequestHandler):


    def prepare(self):
        content_type = self.request.headers.get("Content-Type")
        if content_type and content_type.startswith("application/json"):
            try:
                self.json_args = json.loads(self.request.body)
            except ValueError:
                self.json_args = json.loads('[]')
                print("Failed to parse json body from %s" % self.request.body)
        else:
            self.json_args = None

    @tornado.web.asynchronous
    @gen.coroutine
    def get(self):
        db = self.settings['db']
        cursor = db.account_balances.find()
        balances = []
        while (yield cursor.fetch_next):
            document = cursor.next_object()
            balances.append(AccountBalance.from_db_rep(document))
        self.render("templ_balance.html", balances=balances)

    @tornado.web.asynchronous
    @gen.coroutine
    def post(self):
        params = self.json_args
        institution = None
        balance = None
        for field in params:
            print("Field = %s" % field)
            if field[u'name'] == u'institution':
                institution = field[u'value']
            elif field[u'name'] == u'current_balance':
                balance = field[u'value']

        ab = AccountBalance(institution = institution, balance = balance, last_update = datetime.datetime.utcnow())
        print(">>>>>>>>> %s" % ab)
        db = self.settings['db']
        result = yield db.account_balances.insert(ab.to_motor_create_json())
        print("XXXXXXXX result = %s" % result)
        self.finish()

    def do_insert(self):
        pass