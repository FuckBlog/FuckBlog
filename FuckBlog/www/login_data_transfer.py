# -*- coding: utf-8 -*-
# 2017/1/10 17:15
"""
-------------------------------------------------------------------------------
Function:   暂时性用于处理登陆的cookie转换
Version:    1.0
Author:     SLY
Contact:    slysly759@gmail.com 

code is far away from bugs with the god Animal protecting
               ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
            ┃      ☃      ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃　永无BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛
                  
-------------------------------------------------------------------------------
"""
from config import configs
import hashlib
import asyncio
import time
from models import User
import logging
from errors import APIError,APIPermissionError,APIValueError
from datetime import datetime
COOKIE_NAME = 'FuckYou'
_COOKIE_KEY = configs.session.secret

def user2cookie(user,max_age):
    expires=str(int(time.time()+ max_age))
    s='%s-%s-%s-%s' %(user.id, user.password,expires,_COOKIE_KEY)
    L=[user.id,expires, hashlib.sha1(s.encode('utf-8')).hexdigest()]
    return '-'.join(L)

@asyncio.coroutine
def cookie2user(cookie_str):
    if not cookie_str:
        return None
    try:
        L=cookie_str.split('-')
        # cookie 不全可能有人伪造吧
        if len(L) !=3:
            return None
        uid, expires, sha1= L
        # 超期就让他掉嘿嘿
        if int(expires)<time.time():
            return None
        user=yield from User.find(uid)
        if user is None:
            return None
        s='%s-%s-%s-%s' %(uid,user.password,expires,_COOKIE_KEY)
        if sha1 != hashlib.sha1(s.encode('utf-8')).hexdigest():
            logging.info('invalid sha1')
            return None
        # 密码已经特殊存储过，这里仍要替换转出
        user.password='******'
        return user
    except Exception as e:
        logging.exception(e)
        return None

def check_user_admin_flag(request):
    if request.__user__ is None or not request.__user__.admin_flag:
        raise APIPermissionError('admin only')
    else:
        return True

def get_page_index(page_str):
    p=1
    try:
        p=int(page_str)
    except TypeError:
        pass
    if p <1:
        p=1
    return p

def text2html(text):
    text=str(text)
    # lines = map(lambda s: '<p>%s</p>' % s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'), filter(lambda s: s.strip() != '', text.split('\n')))
    # 为了 配合我的评论也支持md 我去掉了<p></p>否则md 无法正常解析
    # lines = map(lambda s: '%s' % s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'),
    #             filter(lambda s: s.strip() != '', text.split('\n')))
    lines = map(lambda s: '%s' % s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'),
                filter(lambda s: s.strip() != '', text.split('\n')))
    # 我需要换行 来支持我的评论md 功能 原先设计就是一傻逼
    return '\n'.join(lines)
# 注意 传入一个字符串 然后替换其中的某些关键字符
def safe_str(str):
    return str.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')



def datetime_filter(t):
    delta = int(time.time() - t)
    if delta < 60:
        return u'1分钟前'
    if delta < 3600:
        return u'%s分钟前' % (delta // 60)
    if delta < 86400:
        return u'%s小时前' % (delta // 3600)
    if delta < 604800:
        return u'%s天前' % (delta // 86400)
    dt = datetime.fromtimestamp(t)
    return u'%s年%s月%s日' % (dt.year, dt.month, dt.day)


