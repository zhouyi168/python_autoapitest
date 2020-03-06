#!usr/bin/env python
#-*- coding:utf-8 _*-
"""
@author:末夏
@file: mylog.py
@time: 2019/08/26
"""
import logging
from logging.handlers import RotatingFileHandler
import  os
import time
from common import constant
from HTMLTestRunnerNew import HTMLTestRunner
import HTMLTestRunnerNew
class Mylog:
    def __init__(self,logname):
        self.logname=logname
        name=time.strftime('%Y%m%d',time.localtime(time.time()))
        file_path=os.path.join(constant.logs_path,name)
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        self.mylog=logging.getLogger(self.logname)
        self.mylog.setLevel('DEBUG')
        format_stay1="%(levelname)s:%(asctime)s--%(name)s--filename%(filename)s--%(module)s--line%(lineno)d:%(message)s"
        format_stay2="%(levelname)s:%(asctime)s--%(name)s--%(module)s--line%(lineno)d:%(message)s"
        format1=logging.Formatter(format_stay1)
        format2=logging.Formatter(format_stay2)


        #输出到控制台
        self.ch=logging.StreamHandler()
        self.ch.setLevel('DEBUG')
        self.ch.setFormatter(fmt=format2)
        self.mylog.addHandler(self.ch)

        #info输出到文件
        self.info_fh=logging.handlers.RotatingFileHandler(os.path.join(file_path,'info.log'),'a',maxBytes=10*1024*1024,
                backupCount=5,encoding='utf-8')
        self.info_fh.setLevel('INFO')
        self.info_fh.setFormatter(fmt=format1)
        # self.mylog.addHandler(self.info_fh)

        #error输出到文件
        self.error_fh = logging.handlers.RotatingFileHandler(os.path.join(file_path,'error.log'),'a',maxBytes=10*1024*1024,
                backupCount=1,encoding='utf-8')
        self.error_fh.setLevel(logging.ERROR)
        self.error_fh.setFormatter(fmt=format1)
        # self.mylog.addHandler(self.error_fh)
        # self.mylog.removeHandler(self.ch)
    def debug(self,msg):
        self.mylog.addHandler(self.ch)
        self.mylog.debug(msg=msg)
        self.mylog.removeHandler(self.ch)
    def info(self,msg):
        self.mylog.addHandler(self.info_fh)
        self.mylog.info(msg=msg)
        self.mylog.removeHandler(self.info_fh)
    def error(self,msg):
        self.mylog.addHandler(self.error_fh)
        self.mylog.error(msg=msg,exc_info=True)
        self.mylog.removeHandler(self.error_fh)

if __name__=="__main__":
    mylog=Mylog('ZY')
    mylog.info('这是测试')
    mylog.error('程序出错')




    #report输出到文件
    # report_fh=logging.FileHandler




# mylog=Mylog()
#
# def setlevel(level):
#
#     if level=='error':
#         mylog.mylog.addHandler(mylog.error_fh)
#     else:
#         mylog.mylog.addHandler(mylog.info_fh)
#
#     mylog.mylog.addHandler(mylog.ch)
#     mylog.mylog.addHandler(mylog.report_fh)

 # def removelevel(level)   :
 #     if level=='error':
 #         mylog.




