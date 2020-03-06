# -*- coding: utf-8 -*-
# @Time    : 2019/8/22 14:10
# @Author  : zhouy
# @File    : test001_register.py
from common import constant
from common.do_excel import DoExcel
from common.request import Request
import unittest
from ddt import ddt,data
import os
import json
from common.config import Config
from common.mysql import Mysql
from  common.replace import Replace
from common.mylog import Mylog
import time

mylog=Mylog('ZY')
Cookies=None
header=None
api_data=DoExcel(constant.data_xlsx).read_excel('register')
api_url=Config().get_value('database','api_url')
today=time.strftime('%Y-%m-%d',time.localtime(time.time()))

@ddt
class ApiTest(unittest.TestCase):

    def setUp(self):
        pass

    @data(*api_data)
    def test_register(self,case):
        try:
            print('第{}条测试用例：[{}]开始执行'.format(case.case_id,case.title))
            global Cookies,header
            sql="SELECT MobilePhone FROM member where MobilePhone!='' and MobilePhone>'1870000001' ORDER BY MobilePhone  LIMIT 1"
            new=str(int(Mysql().fetchone(sql=sql)[0])-1)
            olddata=Replace().data_replace(case.data,new)
            print(olddata)
            resp=Request(url=api_url+case.url,data=eval(olddata),method=case.method,Cookies=Cookies,header=None)
            if resp.get_cookies():
                Cookies=resp.get_cookies()
            if resp.get_header():
                header=resp.get_header()
            resp_text=json.loads(resp.get_text())
            mylog.info(resp_text)
            actual=resp_text['msg']
            DoExcel(constant.data_xlsx).write_excel('register',case.case_id + 1, 7, actual)

            result = None
            try:
                self.assertEqual(case.expect,actual)
                mylog.info('第{}条测试用例：[{}]断言成功 '.format(case.case_id,case.title))
                result='pass'
                mobilephone = eval(olddata)['mobilephone']
                check_sql = "SELECT MobilePhone FROM member WHERE RegTime BETWEEN '{0} 00:00:00' and '{0} 23:59:59'".format(today)
                regist_phones = Mysql().fetchall(check_sql)
                regist_phone=[]
                for i in regist_phones:
                    regist_phone.append(i[0])
                if actual=='注册成功':
                    try:
                        self.assertIn(mobilephone,regist_phone)
                        mylog.info('第{}条测试用例：[{}]执行结果为：{}'.format(case.case_id, case.title, result))
                        DoExcel(constant.data_xlsx).write_excel('register', case.case_id + 1, 8, result)
                    except AssertionError as e:
                        mylog.error('数据库验证失败')
                        result = 'failed'
                        mylog.info('第{}条测试用例：[{}]执行结果为：{}'.format(case.case_id, case.title, result))
                        DoExcel(constant.data_xlsx).write_excel('register', case.case_id + 1, 8, result)

                elif actual!='注册成功' :
                    try:
                        self.assertIn(mobilephone,regist_phone)
                        result='failed'
                        mylog.info('第{}条测试用例：[{}]执行结果为：{}'.format(case.case_id, case.title, result))
                        DoExcel(constant.data_xlsx).write_excel('register', case.case_id + 1, 8, result)
                    except AssertionError as e:
                        mylog.info('数据库验证成功')
                        result = 'pass'
                        mylog.info('第{}条测试用例：[{}]执行结果为：{}'.format(case.case_id, case.title, result))
                        DoExcel(constant.data_xlsx).write_excel('register', case.case_id + 1, 8, result)

            except AssertionError as e:
                result='failed'
                mylog.info('第{}条测试用例：[{}]断言失败，执行结果为：{}'.format(case.case_id, case.title, result))
                DoExcel(constant.data_xlsx).write_excel('register',case.case_id + 1, 8, result)
                raise e
            finally:
                mylog.info('第{}条测试用例：[{}]执行完毕'.format(case.case_id, case.title))
        except Exception as e:
            print('执行程序异常！')
            raise e
