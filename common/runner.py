# -*- coding: utf-8 -*-
# @Time    : 2019/8/20 11:51
# @Author  : zhouy
# @File    : runner.py

import unittest
from common import constant
import test_cases.test002_login
from test_cases.test002_login import ApiTest
import HTMLTestRunnerNew
import os


suite=unittest.TestSuite()
discover=unittest.defaultTestLoader.discover(constant.testcases_path,pattern='test*.py',top_level_dir=None)

with open(os.path.join(constant.reports_path,'api_test.html'),'wb') as f:
    HTMLTestRunnerNew.HTMLTestRunner(stream=f,verbosity=2,title='Api自动化测试').run(discover)





