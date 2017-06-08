# -*- coding: utf-8 -*-
# 2017/1/12 22:11
"""
-------------------------------------------------------------------------------
Function:
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
import asyncio, logging, json
from aiohttp import web
from urllib import parse
from login_data_transfer import cookie2user
# 老子就是爱用coroutine装饰 你咬我啊

COOKIE_NAME = 'FuckYou'
_COOKIE_KEY = configs.session.secret
@asyncio.coroutine
def logger_factory(app,handler):
    def logger(request):
        logging.info('Request: %s %s' %(request.method, request.path))
        return (yield from handler(request))
    return logger
# 这个下面的很多方法 比如content_type post()方法我还没找奥在哪里
@asyncio.coroutine
def data_factory(app, handler):
     @asyncio.coroutine
     def parse_data(request):
        logging.info('data factory...')
        if request.method in ('POST','PUT'):
            if not request.content_type:
                return web.HTTPBadRequest(text='content_type error!')
            # 弄个小写 我也是醉了
            # 注意 这里如果有str的话 那么startswith 就会高亮

            content_type = str(request.content_type.lower())
            # print(content_type)
            if content_type.startswith('application/json'):
                request.__data__= yield from request.json()
                if not isinstance(request.__data__, dict):
                    return web.HTTPBadRequest(text='must be a json object')

                logging.info('request json %s ' %str(request.__data__))
            elif request.content_type.startswith('application/x-www-form-urlencoded'):
                params = yield from request.post()
                request.__data__=dict(**params)
                logging.info('request from : %s ' %str(request.__data__))
            else:
                return web.HTTPBadRequest(text='Unsupported Content-Type: %s' % content_type)
        elif request.method =='GET':
            qs = request.query_string
            # 这个parse解析函数日后给我查一下
            request.__data__={k : v[0] for k, v in parse.parse_qs(qs,True).items()}
            logging.info('request query: %s' % request.__data__)
        else:
            request.__data__ = dict()
        # 这里可能有问题
        print(dir(request))
        result = yield from handler(request)
        return result
     return parse_data

@asyncio.coroutine
def response_factory(app, handler):
    @asyncio.coroutine
    def response(request):
        logging.info('response handler...')
        r = yield from handler(request)
        if isinstance(r, web.StreamResponse):
            return r
        if isinstance(r, bytes):
            resp=web.Response(body=r)
            resp.content_type = 'application/octet-stream'
            return resp
        if isinstance(r,str):
            if r.startswith('redirect:'):
                # 这个r[9:]没有懂
                return web.HTTPFound(r[9:])
            resp=web.Response(body=r.encode('utf-8'))
            resp.content_type='text/html;charset=utf-8'
            return resp
        if isinstance(r, dict):
            print(r)
            template=r.get('__template__')
            if template is None:
                # 这句话是为了渲染jinjia模板喵 没懂 回过头来看
                resp = web.Response(body=json.dumps(r,ensure_ascii=False,default=lambda o : o.__dict__).encode('utf-8'))
                resp.content_type = 'application/json;charset=utf-8'
                return resp
            else:
                # 如果用jinjia2 渲染，则绑定已经验证过的用户
                r['__user__'] = request.__user__
                resp = web.Response(body=app['__templating__'].get_template(template).render(**r).encode('utf-8'))
                resp.content_type='text/html;charset=utf-8'
                return resp
        if isinstance(r, int) and 100 <= r < 600:
            return web.Response(status=r)
        if isinstance(r,tuple) and len(r):
            status, message=r
            if isinstance(status, int) and 100 <= r < 600:
                return web.Response(status=status, text=str(message))
        resp=web.Response(body=str(r).encode('utf-8'))
        resp.content_type='text/plain;charset=utf-8'
        return resp
    return response
#
# 警告 这个factory是不可用的 需要完善
@asyncio.coroutine
def auth_factory(app, handler):
    @asyncio.coroutine
    def auth(request):
            # 警告 这里request method 可能需要加__method__
            logging.info('check user: %s:%s' % (request.method, request.path))
            request.__user__=None
            # 注意：这里是对COOKIE_NAME的cookie进行验证，而非我们的FakeCookie
            cookie_str=request.cookies.get(COOKIE_NAME)
            # print(cookie_str)
            if cookie_str:
                # 注意： 这里的auth工厂将cookie 信息 经过查询 映射到request.__user__上面
                user=yield from cookie2user(cookie_str)
                if user is not None:
                    logging.info('set current user:%s' %user)
                    request.__user__=user
            if request.path.startswith('/manage') and(request.__user__ is None or not
                                                       request.__user__.admin_flag):
                return web.HTTPFound('/login')
            return (yield from handler(request))
    return auth




