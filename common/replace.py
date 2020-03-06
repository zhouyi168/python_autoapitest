# -*- coding: utf-8 -*-
# @Time    : 2019/8/22 14:35
# @Author  : zhouy
# @File    : replace.py
import re
from common.config import Config
class Replace:
    def data_replace(self,oldpatt,new):
        try:
            result = re.search(r'M{(.*?)}', oldpatt)
            if result:
                result=result.group()
                oldpatt=oldpatt.replace(result,new,1)

        except Exception as e:
            print('没有匹配项',e)

        finally:
            return oldpatt

    def sub_all(self,s):
        while re.search(r'M{(.*?)}', s):
            result=re.search(r'M{(.*?)}',s)

            if hasattr(Context,result.group(1)):
                str = getattr(Context, result.group(1))
                s=re.sub(r'M{(.*?)}',str,s,count=1)
        return s



class Context:
    normal_login=Config().get_value('user','login_name')
    pwd=Config().get_value('user','pwd')
    Cookies = None
    nomal_id=Config().get_value('id','nomal_id')
    loan_id=Config().get_value('id','loan_id')
    admin_user=Config().get_value('user','admin_user')
    admin_pwd=Config().get_value('user','admin_pwd')


if __name__=="__main__":
    data="{'mobilephone':'M{normal_login}', 'pwd': 'M{pwd}', 'regname': '小迷茫'}"
    data1='{"memberId":M{nomal_id},"title":"try+a+test","amount":2000,"loanRate":18.0,"loanTerm":30,"loanDateType:2,"repaymemtWay":5,"biddingDays":5}'
    # new='13526465653'
    # pwd='123456'
    # result=Replace().data_replace(data,new)
    # print(result)
    # result1 = Replace().data_replace(result,pwd)
    # print(result)
    # print(result1)
    # print(Replace().data_replace(data,new))
    # print(Replace().data_replace(data,pwd))
    # normal=getattr(Context,'normal_login')
    # print(normal)
    # login_name=Config().get_value('user','login_name')
    # print(login_name)
    # setattr(Context,'normal_login',login_name)
    # print(getattr(Context,'normal_login'))
    s=Replace()
    print(s.sub_all(data1))




