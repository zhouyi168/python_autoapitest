#!usr/bin/env python
#-*- coding:utf-8 _*-
"""
@author:末夏
@file: test006_audit.py
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
from common.mysql import Mysql

mylog=Mylog('audit').mylog
Cookies=None
header=None
api_data=DoExcel(constant.data_xlsx).read_excel('audit')
api_url=Config().get_value('database','api_url')

@ddt
class ApiTest(unittest.TestCase):
    def setUp(self):
        self.mysql=Mysql()
        # status={'审核中':1,'二审(初审中)':2,'三审(复审中)':3,'竞标中':4,'核保审批':5,'平台终审':6,'还款中':7,'审核不通过':8,'流标':9,'还款完成':10,'申请流标':11}

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
            DoExcel(constant.data_xlsx).write_excel('audit',case.case_id + 1, 7, actual)
            result = None
            olddata=eval(s)
            status_sql = "SELECT status FROM loan where id={0}".format(olddata['id'])
            actual_status = self.mysql.fetchone(status_sql)[0]
            try:
                self.assertEqual(case.expect,actual)
                result='pass'
                if 'id' in olddata.keys():
                    try:
                        self.assertEqual(olddata['status'],int(actual_status))
                        mylog.info('第{}条测试用例：[{}]执行结果为：{}'.format(case.case_id,case.title,result))
                        DoExcel(constant.data_xlsx).write_excel('audit',case.case_id+1,8,result)
                    except AssertionError as e:
                        result='failed'
                        mylog.info('第{}条测试用例：[{}]执行结果为：{}'.format(case.case_id,case.title,result))
                        DoExcel(constant.data_xlsx).write_excel('audit', case.case_id + 1, 8, result)
                        mylog.error('数据库验证失败：{0}'.format(e))
                        raise e
            except AssertionError as e:
                result='failed'
                print('第{}条测试用例：[{}]断言失败，执行结果为：{}'.format(case.case_id, case.title, result))
                DoExcel(constant.data_xlsx).write_excel('audit',case.case_id + 1, 8, result)
                raise e
            finally:
                print('第{}条测试用例：[{}]执行完毕'.format(case.case_id, case.title))
    except Exception as e:
        print('执行程序异常！')
        raise e