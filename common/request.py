#!usr/bin/env python
#-*- coding:utf-8 _*-
"""
@author:末夏
@file: request.py
@time: 2019/08/19
"""
import requests

class Request:
    def __init__(self,method,url,data=None,Cookies=None,header=None):
        try:
            if method=='get':
                self.resp=requests.get(url=url,params=data,cookies=Cookies,headers=header)
            elif method=='post':
                self.resp=requests.post(url=url,data=data,cookies=Cookies,headers=header)
            elif method=='delete':
                self.resp=requests.delete(url=url,data=data,cookies=Cookies,headers=header)
        except Exception as e:
            raise e


    def get_text(self):
        return self.resp.text
    def get_status_code(self):
        return self.resp.status_code
    def get_json(self):
        return self.resp.json()
    def get_cookies(self):
        return self.resp.cookies
    def get_header(self):
        return self.resp.headers

if __name__=="__main__":
    url='http://test.lemonban.com/futureloan/mvc/api/member/login'
    methon='get'
    data={'mobilephone':18684720553, 'pwd': 'python'}
    reps=Request(method=methon,url=url,data=data)
    print(type(reps))
    print(reps.get_text())
    import json
    s=json.loads(reps.get_text(),encoding='utf-8')
    print(s['msg'])

