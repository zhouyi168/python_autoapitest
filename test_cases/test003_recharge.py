# -*- coding: utf-8 -*-
# @Time    : 2019/8/23 17:16
# @Author  : zhouy
# @File    : test003_recharge.py
from common import constant
from common.do_excel import DoExcel
from common.request import Request
import unittest
from ddt import ddt,data
import os
import json
from common.config import Config
from common.replace import Replace,Context
from common.mysql import Mysql
from common.mylog import Mylog
mylog=Mylog('zy')
header=None
api_data=DoExcel(constant.data_xlsx).read_excel('recharge')
api_url=Config().get_value('database','api_url')
@ddt
class RechargeTest(unittest.TestCase):

    def setUp(self):
        phone=Config().get_value('user','login_name')
        self.mysql=Mysql()
        self.leaveAmount_sql="SELECT LeaveAmount FROM member WHERE MobilePhone={0}".format(phone)
        self.leaveAmount=float(self.mysql.fetchone(self.leaveAmount_sql)[0])
    try:
        @data(*api_data)
        def test_api(self,case):
            mylog.info('第{}条测试用例：[{}]开始执行'.format(case.case_id,case.title))
            #print(case.data)
            data=eval(Replace().sub_all(case.data))
            #print(data)
            if hasattr(Context,'Cookies'):
                Cookies=getattr(Context,'Cookies')
            else:
                Cookies=None
            resp=Request(url=api_url+case.url,data=data,method=case.method,Cookies=Cookies,header=None)
            c=resp.get_cookies()
            if c:
                if hasattr(Context,'Cookies'):
                    setattr(Context,'Cookies',c)

            if resp.get_header():
                header=resp.get_header()
            actual=json.loads(resp.get_text())['msg']
            #print(actual)
            DoExcel(constant.data_xlsx).write_excel('recharge',case.case_id + 1, 7, actual)
            result = None
            try:
                self.assertEqual(case.expect,actual)
                result='pass'
                now_leaveAmount=float(Mysql().fetchone(self.leaveAmount_sql)[0])
                if actual == '充值成功':
                    try:
                        actual_amount = self.leaveAmount + data['amount']
                        self.assertEqual(now_leaveAmount,actual_amount)
                        mylog.info('第{}条测试用例：[{}]执行结果为：{}'.format(case.case_id, case.title, result))
                        DoExcel(constant.data_xlsx).write_excel('recharge', case.case_id + 1, 8, result)
                    except AssertionError as e:
                        result = 'failed'
                        mylog.info('第{}条测试用例：[{}]执行结果为：{}'.format(case.case_id, case.title, result))
                        DoExcel(constant.data_xlsx).write_excel('recharge', case.case_id + 1, 8, result)
                        mylog.error('余额数据库验证失败'.format(e))
                elif actual!='充值成功' :
                    try:
                        self.assertEqual(now_leaveAmount,self.leaveAmount)
                        mylog.info('第{}条测试用例：[{}]执行结果为：{}'.format(case.case_id, case.title, result))
                        DoExcel(constant.data_xlsx).write_excel('recharge', case.case_id + 1, 8, result)
                    except AssertionError as e:
                        result = 'failed'
                        mylog.info('第{}条测试用例：[{}]执行结果为：{}'.format(case.case_id, case.title, result))
                        DoExcel(constant.data_xlsx).write_excel('recharge', case.case_id + 1, 8, result)
                        mylog.error('余额数据库验证失败'.format(e))
            except AssertionError as e:
                result = 'failed'
                mylog.info('第{}条测试用例：[{}]断言失败，执行结果为：{}'.format(case.case_id, case.title, result))
                DoExcel(constant.data_xlsx).write_excel('recharge', case.case_id + 1, 8, result)
                raise e
    except Exception as e:
        print('执行程序异常！')
        raise e
