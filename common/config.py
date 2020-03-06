# -*- coding: utf-8 -*-
# @Time    : 2019/8/21 11:03
# @Author  : zhouy
# @File    : config.py

import os
from common import constant
import configparser

class Config:
    def __init__(self):
        self.con=configparser.ConfigParser()
        self.con.read(constant.gloabl_path)
        if self.get_bool('switch','on' ):
            self.con.read(constant.online_path)
        else:
            self.con.read(constant.test_path)

    def get_value(self,section,option):
        return self.con.get(section,option)
    def get_int(self,section,option):
        return self.con.getint(section,option)
    def get_bool(self,section,option):
        return self.con.getboolean(section,option)
    def get_float(self,section,option):
        return self.con.getfloat(section,option)









