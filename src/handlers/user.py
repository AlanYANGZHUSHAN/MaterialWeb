# -*- coding: utf-8  -*-
import logging
import tornado.web
from dbs import user
import json

user_db = None
def init_user_tool(config):
    global user_db
    user_db = user.DBINIT(config)


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        current_user = self.get_secure_cookie('username')
        if current_user:
            return current_user
        return None

class loginHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('login.html')
    def post(self):
        body = self.request.body
        req = json.loads(body, encoding = 'utf-8')
        res = user_db.manage_user(req)
        ret = {
                'status' : res['status'],
                'result' : res["result"],
                'msg'    : res['msg']
                }
        self.set_user_cookie(ret)
        self.write(json.dumps(ret))
    def set_user_cookie(self,ret):
        if ret['status'] == "SUCCESS":
            self.set_secure_cookie("username", ret['result']['username'])
            if ret['result']['record']:
                self.set_secure_cookie("record", 'true')
            else:
                self.set_secure_cookie("record",'false')
            if ret['result']['manager']:
                self.set_secure_cookie("manager", 'true')
            else:
                self.set_secure_cookie('manager','false')
            if ret['result']['query']:
                self.set_secure_cookie("query", 'true')
            else:
                self.set_secure_cookie('query','false')

class registerHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('register.html')
    def post(self):
        body = self.request.body
        req = json.loads(body, encoding = 'utf-8')
        res = user_db.manage_user(req)
        ret = {
                'status' : res['status'],
                'msg'    : res['msg']
                }
        self.write(json.dumps(ret))

class setRightHandler(tornado.web.RequestHandler):
    def post(self):
        body = self.request.body
        req = json.loads(body, encoding = 'utf-8')
        res = user_db.manage_user(req)
        ret = {
                'status' : res['status'],
                'msg'    : res['msg']
                }
        self.write(json.dumps(ret))

class deleteHandler(tornado.web.RequestHandler):
    def post(self):
        body = self.request.body
        req = json.loads(body, encoding = 'utf-8')
        res = user_db.manage_user(req)
        ret = {
                'status' : res['status'],
                'msg'    : res['msg']
                }
        self.write(json.dumps(ret))

class mainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        username = self.get_secure_cookie('username')
        record = self.get_secure_cookie('record')
        manager = self.get_secure_cookie('manager')
        query = self.get_secure_cookie('query')
        self.render('main.html',username=username,record=record,manager=manager,query=query)

 
class getAllHandler(tornado.web.RequestHandler):
    def post(self):
        username = self.get_secure_cookie('username')
        body = self.request.body
        req = json.loads(body, encoding = 'utf-8')
        req['username'] = username
        res = user_db.manage_user(req)
        ret = {
                'result' : res["result"],
                'status' : res['status'],
                'msg'    : res['msg']
                }
        self.write(json.dumps(ret))

class addMaterialHandler(tornado.web.RequestHandler):
    def post(self):
        body = self.request.body
        req = json.loads(body, encoding = 'utf-8')
        res = user_db.manage_user(req)
        ret = {
                'status' : res['status'],
                'msg'    : res['msg']
                }
        self.write(json.dumps(ret))

class getAllMaterialHandler(tornado.web.RequestHandler):
    def post(self):
        body = self.request.body
        req = json.loads(body, encoding = 'utf-8')
        res = user_db.manage_user(req)
        ret = {
                'result' : res["result"],
                'status' : res['status'],
                'msg'    : res['msg']
                }
        self.write(json.dumps(ret))

class storageActionHandler(tornado.web.RequestHandler):
    def post(self):
        body = self.request.body
        req = json.loads(body, encoding = 'utf-8')
        username = self.get_secure_cookie('username')
        req['operator'] = username
        if not isinstance(req['id'],str):
            req['id'] = str(req['id'])
        if isinstance(req['amount'],str):
            req['amount'] = int(req["amount"])
        res = user_db.manage_user(req)
        ret = {
                'status' : res['status'],
                'msg'    : res['msg']
                }
        self.write(json.dumps(ret))

class materialRestHandler(tornado.web.RequestHandler):
    def post(self):
        body = self.request.body
        req = json.loads(body, encoding = 'utf-8')
        res = user_db.manage_user(req)
        ret = {
                'result' : res["result"],
                'status' : res['status'],
                'msg'    : res['msg']
                }
        self.write(json.dumps(ret))

'''class getContentListHandler(tornado.web.RequestHandler):
     def post(self):
         ret = {}
         body = self.request.body
         req = json.loads(body, encoding = 'utf-8')
         res = homepage_db.get_content_list(req)
         ret = {
                 'status' : res["status"],
                 'result' : res["result"],
                 'msg'    : res['msg']
                }
        self.write(json.dumps(ret))

class addOneItemHandler(tornado.web.RequestHandler):
    def post(self):
        ret = {}
        body = self.request.body
        req = json.loads(body, encoding = 'utf-8')
        logging.info(req)
        res = homepage_db.add_one_item(req)
        logging.info(res)
        ret = {
                'status' : res["status"],
                'msg'    : res['msg']
                }
        self.write(json.dumps(ret))

class addOneFileHandler(tornado.web.RequestHandler):
    def post(self):

        ret = {}
        req = self.request.files['file']
        res = homepage_db.add_one_file(req)
        logging.info(res)
        ret = {
                'status' : res["status"],
                'msg'    : res['msg']
                }
        self.write(json.dumps(ret))

class picToEpsHandler(tornado.web.RequestHandler):
    def post(self):

        ret = {}
        body = self.request.body
        req = json.loads(body, encoding = 'utf-8')
        res = homepage_db.pic_to_eps(req)
        logging.info(res)
        ret = {
                'status' : res["status"],
                'To_fileName' : res['To_fileName'],
                'msg'    : res['msg']
                }
        self.write(json.dumps(ret))'''
