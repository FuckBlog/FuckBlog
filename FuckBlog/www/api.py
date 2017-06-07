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
from www.models import User, Comment, Blogs, next_id
from www.base import get, post
from www.base import Page
import time
import re,json
from www.errors import APIError, APIValueError
import hashlib
from aiohttp import  web
from www.config import configs
from www.login_data_transfer import user2cookie, text2html, check_user_admin_flag, get_page_index, safe_str
import base64
import www.markdown2
import logging
from www.login_data_transfer import datetime_filter
COOKIE_NAME = 'FuckYou'
_COOKIE_KEY = configs.session.secret
# 这个逼屌丝直接设置取值哈哈哈 我很好奇她咋绕过数据库
@asyncio.coroutine
@get('/index.html')
def index_test():
    # 这里我想先用js 来处理 而非Python后台
    return {
        '__template__':'index.html'
    }

@get('/')
def index():
    return {
        '__template__':'index.html'
    }

@get('/test.html')
def test():
    return {
        '__template__':'test.html'
    }

@get('/manage/{name}')
def admin_page(name):
# 我发现一旦请求非html 的就会报错 那么我需要限定html 文件访问
    if '.html' in str(name):
        return {
            "__template__":name
        }

    else:
        return {
            "__template__":'index_test.html'
        }
@asyncio.coroutine
@get('/api/users')
def api_get_users(request):
    # 所有涉及核心数据输出都需要检查admin_flag
    check_user_admin_flag(request)
    users = yield from User.find_all(orderBy='created_time desc')
    for u in users:
        u.password = '******'
    return dict(data=users)

# @get('/api/{tag}')
# def get_tag_article(*, tag):
#     blog=yield from Blogs.find_all('tag=?', [tag])
#     return dict(blogs=blog)


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
                image='/static/images/default-user.jpg' )
    # % hashlib.md5(email.encode('utf-8')).hexdigest()
    yield from user.save()
    r=web.Response()
    encode_str=user.name+'-'+user.email
    fake_string=base64.b64encode(encode_str.encode(encoding="utf-8"))
    r.set_cookie('FakeCookie', fake_string.decode('utf-8'), max_age=86400, httponly=False)
    r.set_cookie(COOKIE_NAME,user2cookie(user, 86400), max_age=86400, httponly=True)
    r.body=json.dumps(user, ensure_ascii=False).encode('utf-8')
    return r

@get('/register')
def register():
    return {
        '__template__':'register.html'
    }

@get('/login')
def login(request):
    # 如果已经登录，那么就定向到首页
    if request.__user__ is not None:
        return {
            '__template__': 'index.html'
        }
    else:
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
    # 这个http only 是为了防止跨域 xss 漏洞
    # 很尴尬的是 我弃用jinja模板现在又要给他启用 否则我要启用session验证（原因是为了安全）
    encode_str=user.name+'-'+user.email
    fake_string=base64.b64encode(encode_str.encode(encoding="utf-8"))
    r.set_cookie('FakeCookie', fake_string.decode('utf-8'), max_age=86400, httponly=False)
    r.set_cookie(COOKIE_NAME,user2cookie(user, 86400), max_age=86400, httponly=True)
    # 我测试看能不能设置多个cookie 一个仅仅用于前端的某些显示使用 结果证实是可以的 我可以不用session验证啦
    user.password='******'
    r.content_type='application/json'
    r.body = json.dumps(user,ensure_ascii=False).encode('utf-8')
    # 有点意思 其实这里用dict 返回一样可以被jinja 模板给encode 被js 解析
    return r

@get('/signout')
def signout(request):
    referer = request.headers.get('Referer')
    # 退回原先访问
    r = web.HTTPFound(referer or '/index.html')
    r.set_cookie('FakeCookie', '-deleted-', max_age=0, httponly=False)
    r.set_cookie(COOKIE_NAME,'-deleted-',max_age=0, httponly=True)
    logging.info('user signed out.')
    return r


# @asyncio.coroutine
# @get('/blog/{id}')
# def get_blog(id):
#     blog = yield from Blogs.find(id)
#     comments = yield from Comment.find_all('blog_id=?', [id], orderBy='created_time desc')
#     for c in comments:
#         c.html_content = text2html(c)
#     blog.html_content = www.markdown2.markdown(blog.content)
#     return {
#         '__template__':'article_test.html',
#         'blog':blog,
#         'comments':comments
#     }

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

# 具体文章API 及其评论
@asyncio.coroutine
@get('/api/blogs/{id}')
def api_get_blog(*, id):
    blog = yield from Blogs.find(id)
    comments = yield from Comment.find_all('blog_id=?', [id], orderBy='created_time desc')
    if comments:
        for c in comments:
            # 这里说明一下原来是str 转html  我改成text2md 如果确认没有xss 情况我换转回来
            # 在我的测试下 发现 存在xss 因此 我想先进行危险字符转译 然后在markdown 解析
            # 但是此时我又想 如果评论中代码需要有如<script 该如何是好？ 我发现转译后 还不错具体可以看text2html的代码
            # c.html_content = text2html(c['content'])
            fuck_xss=text2html(c['content'])
            c.html_content=www.markdown2.markdown(fuck_xss)
    if hasattr(blog,'content'):
        blog.html_content = www.markdown2.markdown(blog.content)
    else:
        blog=dict()
        blog['html_content']='<h1>404 not found</h1>'
        blog['blog_title']='不好意思 你要的页面无法找到'
        blog['user_name']='无名氏'
        blog['created_time']='1484186522.78509'
        blog['tag']='*'
    return dict(blogs=blog, comments=comments)

# 文章发布API
@post('/api/blogs')
def api_create_blog(request,* ,blog_title, blog_tag, summary, content):
    check_user_admin_flag(request)
    if not blog_title or not blog_title.strip():
        raise APIValueError('blog_title','blog_title can not be empty')
    if not summary or not summary.strip():
        raise APIValueError('summary','summary can not be empty')
    if not content or not content.strip():
        raise APIValueError('content','content can not be empty')
    if not blog_tag or not blog_tag.strip():
        blog_tag='默认分类'
    # 注意 这里请求了request 的user 等信息 实际上是因为在上面进行了确认
    blog = Blogs(user_id=request.__user__.id, user_name=request.__user__.name,user_image=request.__user__.image, blog_title=blog_title.strip(), summary=summary.strip(), content=content.strip(), tag=blog_tag)
    yield from blog.save()
    # 现在需要新增一个 保存后返回文章链接的功能
    blogs = yield from Blogs.find_all(OrderBy='created_at desc')
    recent_blog=blogs[-1]
    blog_url='/index.html?item='+recent_blog['id']
    return {'new_url':blog_url}
# 评论发布API
# def api_create_comment(request):
#     return
# 按page 或者 分类目录  请求API
@get('/api/blogs')
def api_blogs(*, page='1', tag='%'):
    # 注意 一般传输过程中 需要将str 的字符串改为int
    page_index=get_page_index(page)
    if tag != '%':
        blogs = yield from Blogs.find_all('tag like ?', [tag],OrderBy='created_at desc')
        if blogs:
            article_nums=len(blogs)
        else:
            article_nums=0
    else:
        article_nums=yield from Blogs.findNumber('count(id)')
        p = Page(article_count=article_nums, index=page_index)
        blogs = yield from Blogs.find_all(OrderBy='created_at desc', limit=(p.offset, p.limit))

    p = Page(article_count=article_nums, index=page_index)
    if article_nums==0:
        return dict(page=p, blogs=())
    return dict(page=p, blogs=blogs)

# 获取博客所有文章
@get('/api/all_blogs')
def get_allblogs():
    blogs=yield from Blogs.find_all(OrderBy='created_at desc')
    return dict(data=blogs)

# 获取博客所有评论
@asyncio.coroutine
@get('/api/all_comt')
def get_allcomt():
    comts=yield from Comment.find_all(OrderBy='created_at desc')
    if comts:
        for comt in comts:
            comt.content=safe_str(comt.content)
            find_blog=yield from Blogs.find(comt.blog_id)
            comt['blog_title']=find_blog.blog_title
            comt.created_time=datetime_filter(comt.created_time)
    else:
        return dict(data='')

    return dict(data=comts)

# 根据tag 来选择文章
@get('/api/tags')
def get_all_tags():
    from www.webframe import orm
    # 不好意思 我已经不想新增一个orm 我绕过orm 设置的args 限制 直接运行我的sql语句
    # 虽然有点不安全 比如有权限获得我的FTP 然后修改这句话 获取数据库的用户信息啥的
    tag=yield from orm.select('select distinct(tag) from blogs')
    return dict(tags=tag)


# 用户新建评论的API
@post('/api/blogs/{id}/comment')
@asyncio.coroutine
def post_comment(id, request, *, content):
    user = request.__user__
    blog = yield from Blogs.find(id)
    if not content or not content.strip():
        raise APIValueError('content', 'content can not be empty')
    if blog is None:
        raise APIValueError('BLOG','BLOG was not found, do not fu*k this site')
    new_content=content
    comment=Comment(blog_id=blog.id,user_id=user.id,user_name=user.name, user_image=user.image, content=new_content)
    yield from comment.save()
    return dict(status='success')




