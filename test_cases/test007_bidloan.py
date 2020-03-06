#!usr/bin/env python
#-*- coding:utf-8 _*-
"""
@author:末夏
@file: test007_bidloan.py
@time: 2019/08/28
"""
from common import constant
from common.do_excel import DoExcel
from common.request import Request
import unittest
from ddt import ddt,data
import os
import json
from common.config import Config
from common.replace import Replace
from common.mylog import Mylog

mylog=Mylog('bidLoan').mylog
Cookies=None
header=None
api_data=DoExcel(constant.data_xlsx).read_excel('bidLoan')
api_url=Config().get_value('database','api_url')

@ddt
class ApiTest(unittest.TestCase):
    try:
        @data(*api_data)
        def test_api(self,case):
            mylog.info('第{}条测试用例：[{}]开始执行'.format(case.case_id,case.title))
            s=Replace().sub_all(case.data)
            global Cookies,header
            resp=Request(url=api_url+case.url,data=eval(s),method=case.method,Cookies=Cookies,header=None)
            if resp.get_cookies():
                Cookies=resp.get_cookies()
            if resp.get_header():
                header=resp.get_header()
            resp_text=json.loads(resp.get_text())
            mylog.info(resp_text)
            actual=resp_text['msg']
            DoExcel(constant.data_xlsx).write_excel('bidLoan',case.case_id + 1, 7, actual)
            result = None
            try:
                self.assertEqual(case.expect,actual)
                result='pass'
                print('第{}条测试用例：[{}]执行结果为：{}'.format(case.case_id,case.title,result))
                DoExcel(constant.data_xlsx).write_excel('bidLoan',case.case_id+1,8,result)
            except AssertionError as e:
                result='failed'
                print('第{}条测试用例：[{}]断言失败，执行结果为：{}'.format(case.case_id, case.title, result))
                DoExcel(constant.data_xlsx).write_excel('bidLoan',case.case_id + 1, 8, result)
                raise e
            finally:
                print('第{}条测试用例：[{}]执行完毕'.format('bidLoan',case.case_id, case.title))
    except Exception as e:
        print('执行程序异常！')
        raise e