# -*- coding: utf-8 -*-
# 2017/1/7 17:41
"""
-------------------------------------------------------------------------------
Function:
Version:    1.0
Author:     SLY
Contact:    slysly759@gmail.com 

code is far away from bugs with the god animal protecting
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

from www.orm import Model, TextField, BooleanField, IntegerField, FloatField, StringField

import time,uuid,random
def next_id():
    return '%s%d' % (int(time.time() * 1000),random.randint(0000,10000))

class User(Model):
    # 这个名字要和数据库字段建立的一毛一样
    __table__='users'
    id=StringField(primary_key=True, default=next_id)
    name=StringField()
    # password 一律sha 加盐处理 后来发现实现上面的确是这样
    password=StringField()
    email=StringField()
    admin_flag=BooleanField()
    image=StringField()
    created_time=FloatField(default=time.time)

class Blogs(Model):
    __table__='blogs'
    id=StringField(primary_key=True, default=next_id)
    user_id=StringField()
    user_name=StringField()
    user_image=StringField()
    blog_title=StringField()
    summary=StringField()
    content=TextField()
    created_time=FloatField(default=time.time)

class Comment(Model):
    __table__='comments'
    id=StringField(primary_key=True, default=next_id)
    blog_id=StringField()
    user_id=StringField()
    user_name=StringField()
    user_image=StringField()
    content=TextField()
    created_time=FloatField(default=time.time)
