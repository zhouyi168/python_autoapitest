# -*- coding: utf-8 -*-
# @Time    : 2019/8/22 11:37
# @Author  : zhouy
# @File    : mysql.py
import pymysql
from common import constant
from common.config import Config
from common.mylog import Mylog

mylog=Mylog('mysql').mylog
class Mysql:
    def __init__(self):
        cf=Config()
        host=cf.get_value('database','host')
        user=cf.get_value('database','user')
        password=cf.get_value('database','pwd')
        database=cf.get_value('database','dbname')
        port=cf.get_int('database','port')
        try:
            self.con=pymysql.connect(host=host, user=user, password=password,
                 database=database, port=port)
        except Exception as e:
            mylog.error('数据库连接有误 ',e)
            raise e
    def fetchone(self,sql):
        cursor=self.con.cursor()
        try:
            cursor.execute(sql)
            return cursor.fetchone()
        except Exception as e:
            mylog.error('执行数据库语句异常',e)
            raise e



    def fetchall(self,sql):
        cursor=self.con.cursor()
        try:
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as e:
            mylog.error('执行数据库语句异常',e)
            raise e

if __name__=="__main__":
    sql="SELECT MobilePhone FROM member WHERE RegTime BETWEEN '2019-05-07 00:00:00' and '2019-05-07 23:59:59'"
    print(int(Mysql().fetchone(sql)[0])+1)
    result=Mysql().fetchall(sql)
    for i in result:        
        print(i[0])
