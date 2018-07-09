# -*- coding: utf-8  -*-
import logging
import pymysql
import datetime
import json
from PIL import Image
import os

ADDUSER      = 'add'
SETUSERRIGHT = 'set'
DELETEUSER   = 'del'
GETUSER      = 'get'
GETALLUSER   = 'getall'
ADDMATERIAL  = 'addmat'
GETALLMAT    = 'getallmat'
STORAGE      = 'storage'
MATERIALREST = 'rest'
class DBINIT(object):
    def __init__(self, config):
        self.config = config
        self.user_conn = pymysql.connect(**self.config["user_db"]) 

    @property
    def conn_user(self):
        self.user_conn.cursorclass = pymysql.cursors.DictCursor
        self.user_conn.ping(True)
        return self.user_conn

    def manage_user(self,req):
        res = {}
        res['status'] = 'FAIL'
        res['msg'] = ''
        if req['action'] == ADDUSER:
            res = self.add_user(req)
        elif req['action'] == SETUSERRIGHT:
            res = self.set_user_right(req)
        elif req['action'] == DELETEUSER:
            res = self.delete_user(req)
        elif req['action'] == GETUSER:
            res = self.get_user(req)
        elif req['action'] == GETALLUSER:
            res = self.get_all_user(req)
        elif req['action'] == ADDMATERIAL:
            res = self.add_material(req)
        elif req['action'] == GETALLMAT:
            res = self.get_all_material(req)
        elif req['action'] == STORAGE:
            res = self.storage_action(req)
        elif req['action'] == MATERIALREST:
            res = self.material_rest(req)
        else:
            res['msg'] += 'invalid action'
        return res

    def add_user(self,req):
        res = {}
        res['status'] = 'FAIL'
        res['msg'] = ''
        if not self.is_valid_user(req):
            res['msg'] += 'invalid user name or invalid password'
            return res
        try:
            if self.is_exist_user(req):
                res['msg'] += 'This user exist'
                return res
            with self.conn_user as cur:
                sql_insert_cmd = "insert into user_info(username,password,position) values(%s,%s,%s)"
                params = [req['username'],req['password'],req['position']]
                cur.execute(sql_insert_cmd,params)
            res['status'] = 'SUCCESS'
        except Exception as e:
            res['msg'] += str(e)
            logging.info('add user is fail')
        return res

    def set_user_right(self,req):
        res = {}
        res['status'] = 'FAIL'
        res['msg'] = ''
        if not self.is_valid_user(req):
            res['msg'] += 'invalid user name or invalid password'
            return res
        try:
            if not self.is_exist_user(req):
                res['msg'] += 'This user not exist'
                return res
            with self.conn_user as cur:
                sql_update_cmd = "update user_info set password= %s,position= %s,record= %s,query= %s,manager= %s where username= %s"
                params = [req['password'],req['position'],req['record'],req['query'],req['manager'],req['username']]
                cur.execute(sql_update_cmd,params)
            res['status'] = 'SUCCESS'
        except Exception as e:
            res['msg'] += str(e)
            logging.info('set user right is fail')
        return res

    def delete_user(self,req):
        res = {}
        res['status'] = 'FAIL'
        res['msg'] = ''
        if not self.is_valid_user(req):
            res['msg'] += 'invalid user name or invalid password'
            return res
        try:
            if not self.is_exist_user(req):
                res['msg'] += 'This user not exist'
                return res
            with self.conn_user as cur:
                sql_delete_cmd = "delete from user_info where username= %s and password= %s"
                params = [req['username'],req['password']]
                cur.execute(sql_delete_cmd,params)
            res['status'] = 'SUCCESS'
        except Exception as e:
            res['msg'] += str(e)
            logging.info('delete user right is fail')
        return res

    def get_user(self,req):
        res = {}
        res['status'] = 'FAIL'
        res['msg'] = ''
        res['result'] = {}
        if not self.is_valid_user(req):
            res['msg'] += 'invalid user name or invalid password'
            return res
        try:
            res['result'] = self.is_exist_user(req)
            if not res['result']:
                res['msg'] += 'This user not exist'
                return res
            res['status'] = 'SUCCESS'
        except Exception as e:
            res['msg'] += str(e)
            logging.info('get user is fail')
        return res

    def is_valid_user(self,req):
        if not req['username'] or not req['password']:
            return False
        return True

    def is_exist_user(self,req):
        with self.conn_user as cur:
            sql_select_cmd = "select * from user_info where username = %s and password = %s"
            params = [req['username'],req['password']]
            cur.execute(sql_select_cmd,params)
            return cur.fetchone()

    def get_all_user(self,req):

        res = {}
        res['status'] = 'FAIL'
        res['msg'] = ''
        res['result'] = []
        try:
            with self.conn_user as cur:
                sql_select_cmd = "select * from user_info where username != %s"
                params = [req['username']]
                cur.execute(sql_select_cmd,params)
                for item in cur.fetchall():
                    res['result'].append(item)
                res['status'] = 'SUCCESS'
        except Exception as e:
            res['msg'] += str(e)
            logging.info('get all user is fail')
        return res

    def add_material(self,req):
        res = {}
        res['status'] = 'FAIL'
        res['msg'] = ''
        try:
            with self.conn_user as cur:
                sql_select_cmd = "select id from material_info where materialname=%s and manufacturer=%s and level=%s and color=%s and width=%s and thick=%s"
                params = [req['materialname'],req['manufacturer'],req['level'],req['color'],req['width'],req['thick']]
                cur.execute(sql_select_cmd,params)
                if cur.fetchone():
                    res['msg'] += 'this material is exist,id is %s'%cur.fetchone()['id']
                    return res
                sql_insert_cmd = "insert into material_info(materialname,manufacturer,level,color,width,thick) values(%s,%s,%s,%s,%s,%s)"
                params = [req['materialname'],req['manufacturer'],req['level'],req['color'],req['width'],req['thick']]
                cur.execute(sql_insert_cmd,params)
                sql_insert_cmd = "insert into material_sum(id,insum,outsum,sum) values(%s,0,0,0)"
                params = [int(cur.lastrowid)]
                cur.execute(sql_insert_cmd,params)
                res['status'] = 'SUCCESS'
        except Exception as e:
            res['msg'] += str(e)
            logging.info('add material is fail')
        return res

    def get_all_material(self,req):
        res = {}
        res['status'] = 'FAIL'
        res['msg'] = ''
        res['result'] = []
        try:
            with self.conn_user as cur:
                sql_select_cmd = "select * from material_info order by id desc"
                cur.execute(sql_select_cmd)
                for item in cur.fetchall():
                    res['result'].append(item)
                res['status'] = 'SUCCESS'
        except Exception as e:
            res['msg'] += str(e)
            logging.info('get all material is fail')
        return res

    def storage_action(self,req):
        res = {}
        res['status'] = 'FAIL'
        res['msg'] = ''
        try:
            with self.conn_user as cur:
                sql_select_cmd = "select * from material_sum where id=%s"
                params = [req['id']]
                cur.execute(sql_select_cmd,params)
                item = cur.fetchone()
                if req['direction'] =='in':
                    params = [item['insum']+req['amount'],item['outsum'],item['sum']+req['amount'],req['id']]
                else:
                    params = [item['insum'],item['outsum']+req['amount'],item['sum']-req['amount'],req['id']]
                if params[2]<0:
                    res['msg'] += 'stroage rest not enough'
                    return res
                sql_update_cmd = "update material_sum set insum= %s,outsum=%s,sum=%s where id=%s"
                cur.execute(sql_update_cmd,params)
                sql_insert_cmd = "insert into material_use(id,action,amount,batch_number,operator) values(%s,%s,%s,%s,%s)"
                params = [req['id'],req['direction'],req['amount'],req['batch_number'],req['operator']]
                cur.execute(sql_insert_cmd,params)
            res['status'] = 'SUCCESS'
        except Exception as e:
            res['msg'] += str(e)
            logging.info('storage action is fail')
        return res

    def material_rest(self,req):

        res = {}
        res['status'] = 'FAIL'
        res['msg'] = ''
        res['result'] = {}
        req['id_list'].sort()
        for id_item in req['id_list']:
            res['result'][id_item] ={'in':[],'out':[],'insum':0,'outsum':0,'sum':0}
        try:
            with self.conn_user as cur:
                sql_insert_cmd = "select * from material_use where id in (%s)"% ','.join(['%s'] * len(req['id_list']))
                params = req['id_list']
                cur.execute(sql_insert_cmd,params)
                for item in cur.fetchall():
                    item['time'] = item['time'].strftime("%Y-%m-%d %H:%M:%S")
                    res['result'][item['id']][item['action']].append(item)
                sql_select_cmd = "select * from material_sum where id in (%s)"%','.join(['%s']*len(req['id_list']))
                params = req['id_list']
                cur.execute(sql_select_cmd,params)
                for item in cur.fetchall():
                    res['result'][item['id']]['insum'] = item['insum']
                    res['result'][item['id']]['outsum'] = item['outsum']
                    res['result'][item['id']]['sum'] = item['sum']
            temp = []
            for item in req['id_list']:
                if item in res['result']:
                    res['result'][item]['id'] = item
                    temp.append(res['result'][item])
            res['result'] = temp
            res['status'] = 'SUCCESS'
        except Exception as e:
            res['msg'] += str(e)
            logging.info('material rest is fail')
        return res


    '''def get_content_list(self, req):
        res = {}
        result_list = []
        res['status'] = 'FAIL'
        res['msg'] = ''
        res['result'] = result_list
        req["start_date"] += ' 00:00:00'
        req["end_date"] += ' 23:59:59'
        try:
            with self.conn_blog as cur:
                if req['tag'] != '--select tag--':
                    sql_select_cmd = "select id,title,create_time,author,tag,url from content_list where create_time >= %s and create_time <= %s and tag = %s"
                    params = [req["start_date"], req["end_date"],req['tag']]
                else:
                    sql_select_cmd = "select id,title,create_time,author,tag,url from content_list where create_time >= %s and create_time <= %s"
                    params = [req["start_date"], req["end_date"]]
                cur.execute(sql_select_cmd, params)
            for row in cur.fetchall():
                item = {}
                item["id"] = row["id"]
                item["title"] = row["title"]
                item["create_time"] = row["create_time"].strftime('%Y-%m-%d %H:%M:%S')
                item["author"] = row["author"]
                item["tag"] = row["tag"]
                item["url"] = row["url"]
                result_list.append(item)
            res['result'] = result_list
            res['status'] = 'SUCCESS'
        except Exception,e:
            res['msg'] += str(e)
            logging.info('get content list is fail')
        return res

    def add_one_item(self, req):
        res = {}
        res['status'] = 'FAIL'
        res['msg'] = ''
        if req['tag'] == '--select tag--':
            res['msg'] += "please select tag"
            return res
        try:
            with self.conn_blog as cur:
                sql_del_cmd = "delete from content_list where url = %s"
                params = [req["url"]]
                cur.execute(sql_del_cmd, params)
                sql_insert_cmd = "insert ignore into content_list(title, author, tag, url) values (%s,%s,%s,%s)"
                params = [req["title"], req["author"], req["tag"], req["url"]]
                cur.execute(sql_insert_cmd, params)

            res['status'] = 'SUCCESS'
        except Exception,e:
            res['msg'] += str(e)
            logging.info('add one item is fail')
        return res

    def add_one_file(self, req):
        res = {}
        res['status'] = 'FAIL'
        res['msg'] = ''
        try:
            for item in req:
                f = open(self.config["static"]+'/myhtml/'+item['filename'],"w")
                f.write(item['body'])
                f.close()

            res['status'] = 'SUCCESS'
        except Exception,e:
            res['msg'] += str(e)
            logging.info('add one file is fail')
        return res


    def pic_to_eps(self,req):
        res = {}
        res['status'] = 'FAIL'
        res['msg'] = ''
        res['To_fileName'] = ''
        try:
            file_path = self.config["static"]+'/myhtml/'
            logging.info(file_path)
            logging.info(req['From_fileName'])
            img = Image.open(file_path+req['From_fileName'])
            img=img.convert("RGB")
            res['To_fileName'] = os.path.splitext(req['From_fileName'])[0]+'.eps'
            logging.info(res['To_fileName'])
            img.save(file_path+res['To_fileName'])
            res['status'] = 'SUCCESS'
        except Exception,e:
            res['msg'] += str(e)
            logging.info('pic to eps is fail')
        return res'''



