# -*- coding: utf-8 -*-
# 2017/1/9 14:10
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
import asyncio
from www.models import User,Comment,Blogs,next_id
from www.base import get,post
from www.base import Page
import time
import re,json
from www.errors import APIError, APIValueError
import hashlib
from aiohttp import  web
from www.config import configs
from www.login_data_transfer import user2cookie, text2html, check_user_admin_flag, get_page_index

import www.markdown2
import logging
COOKIE_NAME = 'FuckYou'
_COOKIE_KEY = configs.session.secret
# 这个逼屌丝直接设置取值哈哈哈 我很好奇她咋绕过数据库
@get('/')
def index():
    summary = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
    # 这里是先伪造数据
    blogs = [
        Blogs(id='1', name='Test Blog', summary=summary, created_at=time.time()-120),
        Blogs(id='2', name='Something New', summary=summary, created_at=time.time()-3600),
        Blogs(id='3', name='Learn Swift', summary=summary, created_at=time.time()-7200)
    ]
    return {
        '__template__': 'blogs.html',
        'blogs': blogs,
    }
@get('/index.html')
def index_test():
    return {
        '__template__':'index.html'
    }
@get('/test.html')
def test():
    return {
        '__template__':'test.html'
    }
# 查一下 这个屌丝程序为何老是需要request

@asyncio.coroutine
@get('/api/users')
def api_get_users():
    users = yield from User.find_all(orderBy='created_time desc')
    for u in users:
        u.password = '******'
    return dict(data=users)

_re_email=re.compile(r'^[a-z0-9\.\-\_]+\@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$')
_re_sha1=re.compile(r'^[0-9a-f]{40}$')

# 这里说明 前后端验证都很重要
@post('/api/users')
def api_register_user(*, email, name, password):
    if not name or not name.strip():
        raise APIValueError('name')
    if not password or not _re_sha1.match(password):
        raise APIValueError('password')
    if not email or not _re_email.match(email):
        raise APIValueError('email')
    users= yield from User.find_all('email=?',[email])
    # 排除注册过的email
    if len(users)>0:
        raise APIError('register failed ','email','The email has already existed')
    uid=next_id()
    row_password_string='%s:%s' %(uid, password)
    # 这个email 是因为用了gravatar的服务 只要email在上面有头像 你的博客里面就可以出现了 虽然没有什么叼用
    user = User(id=uid,name=name.strip(),email=email,password=hashlib.sha1(row_password_string.encode('utf-8')).hexdigest(),
                image='http://www.gravatar.com/avatar/%s?d=mm&s=120' % hashlib.md5(email.encode('utf-8')).hexdigest())
    print(user)
    yield from user.save()
    r=web.Response()
    r.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400, httponly=True)
    r.body=json.dumps(user, ensure_ascii=False).encode('utf-8')
    return r

@get('/register')
def register():
    return {
        '__template__':'register.html'
    }

@get('/login')
def login():
    return{
        '__template__':'login.html'
    }
@get('/sign')
def sign():
    return {
        '__template__':'sign.html'
    }
@asyncio.coroutine
@post('/api/authenticate')
def authenticate(*, email, password):
    if not email:
        raise APIValueError('email')
    if not password:
        raise APIValueError('password')
    users= yield from User.find_all('email=?',[email])
    if len(users)==0:
        raise APIValueError('email','email not found')
    user=users[0]
    sha1=hashlib.sha1()
    # 这里根据加密方式还原
    sha1.update(user.id.encode('utf-8'))
    sha1.update(':'.encode('utf-8'))
    sha1.update(password.encode('utf-8'))
    if user.password != sha1.hexdigest():
        raise APIValueError('password','Invalid password')
    # 确认ok那么就开始设置cookie
    r=web.Response()
    # 这个http only还要看一下 什么鬼设置
    r.set_cookie(COOKIE_NAME,user2cookie(user, 86400), max_age=86400, httponly=True)
    user.password='******'
    r.content_type='application/json'
    r.body = json.dumps(user,ensure_ascii=False).encode('utf-8')
    return r

@get('/signout')
def signout(request):
    referer = request.headers.get('Referer')
    # 退回原先访问
    r = web.HTTPFound(referer or '/')
    r.set_cookie(COOKIE_NAME,'-deleted-',max_age=0, httponly=True)
    logging.info('user signed out.')
    return r

@asyncio.coroutine
@get('/blog/{id}')
def get_blog(id):
    blog = yield from Blogs.find(id)
    comments = yield from Comment.find_all('blog_id=?', [id], orderBy='created_time desc')
    for c in comments:
        c.html_content = text2html(c)
    blog.html_content = www.markdown2.markdown(blog.content)
    return {
        '__template__':'blog.html',
        'blog':blog,
        'comments':comments
    }
@get('/manage')
def manage_admin():
    return {
        '__template__':'/index_test.html'
    }

@get('/manage/blogs/create')
def manage_create_blog():
    return {
        '__template__':'manage_blog_create.html',
        'id':'',
        'action':'/api/blogs'
    }

@get('/api/blogs/{id}')
def api_get_blog(*, id):
    blog = yield from Blogs.find(id)
    return blog

@post('/api/blogs')
def api_create_blog(request,* ,blog_title, summary, content):
    check_user_admin_flag(request)
    if not blog_title or not blog_title.strip():
        raise APIValueError('blog_title','blog_title can not be empty')
    if not summary or not summary.strip():
        raise APIValueError('summary','summary can not be empty')
    if not content or not content.strip():
        raise APIValueError('content','content can not be empty')
    # 注意 这里请求了request 的user 等信息 我担心在实际过程中没有获取到
    blog = Blogs(user_id=request.__user__.id, user_name=request.__user__.name,user_image=request.__user__.image, blog_title=blog_title.strip(), summary=summary.strip(), content=content.strip())
    yield from blog.save()
    return blog

@get('/api/blogs')
def api_blogs(*, page='1'):
    # 注意 一般传输过程中 需要将str 的字符串改为int
    page_index=get_page_index(page)
    article_nums=yield from Blogs.findNumber('count(id)')
    p=Page(article_count=article_nums, index=page_index)
    if article_nums==0:
        return dict(page=p, blogs=())
    blogs=yield from Blogs.find_all(OrderBy='created_at desc', limit=(p.offset, p.limit))
    return dict(page=p, blogs=blogs)
