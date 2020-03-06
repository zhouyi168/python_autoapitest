#!usr/bin/env python
#-*- coding:utf-8 _*-
"""
@author:末夏
@file: constant.py
@time: 2019/08/19
"""

import os
basic_path=os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]

common_path=os.path.join(basic_path,'common')
conf_path=os.path.join(basic_path,'conf')
datas_path=os.path.join(basic_path,'datas')
data_xlsx=os.path.join(datas_path,'data.xlsx')
logs_path=os.path.join(basic_path,'logs')
reports_path=os.path.join(basic_path,'reports')
testcases_path=os.path.join(basic_path,'test_cases')
assert_path=os.path.join(basic_path,'assertions')


#配置文件路径
online_path=os.path.join(conf_path,'online.conf')
test_path=os.path.join(conf_path,'test.conf')
gloabl_path=os.path.join(conf_path,'gloabe.conf')
data_case=os.path.join(conf_path,'data_case.conf')

#url路径

