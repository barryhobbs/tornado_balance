#!/usr/bin/env python
#
# Copyright 2009 Facebook
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
import logging
import os

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import motor
from tornado.options import define, options

from handlers import balance_handler, user_handler, institution_handler, institution_types_handler

define("port", default=8888, help="run on the given port", type=int)


class MainHandler(tornado.web.RequestHandler):
    logger = logging.getLogger("balance")
    logger.setLevel(10)

    def get(self, *args, **kwargs):
        print("Get called in MainHandler")
        self.render("templ_main.html")


def main():
    tornado.options.parse_command_line()
    db = motor.MotorClient().balance_database
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/balances", balance_handler.BalanceHandler),
        (r"/users", user_handler.UserHandler),
        (r"/institutions", institution_handler.InstitutionHandler),
        (r"/institution_types", institution_types_handler.InstitutionTypesHandler)
    ], debug=True, static_path=os.path.join(os.path.dirname(__file__), "static"), db=db)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
