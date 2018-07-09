# -*- coding: utf-8  -*-
import tornado.ioloop
import tornado.web
import tornado.httpserver
import logging
from handlers.user import *

def start_http(config):
    init_user_tool(config)
    settings = {
        "cookie_secret": "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
        "login_url"    : "/login",
        "debug"        :True
        }
    application = tornado.web.Application([
        (r'/static/(.*)', tornado.web.StaticFileHandler, {"path":config['static']}),
        (r"/login", loginHandler),
        (r"/register", registerHandler),
        (r"/setright", setRightHandler),
        (r"/delete", deleteHandler),
        (r"/main", mainHandler),
        (r"/getall", getAllHandler),
        (r"/addmaterial", addMaterialHandler),
        (r"/getallmaterial", getAllMaterialHandler),
        (r"/storageaction", storageActionHandler),
        (r"/rest", materialRestHandler),

        ],
        **settings
        )
    application.settings["template_path"] = config["templates"]
    server = tornado.httpserver.HTTPServer(application)
    server.listen(config["http_port"],config["http_host"])
    ioloop = tornado.ioloop.IOLoop.instance()
    print("ioloop start")
    ioloop.start()
