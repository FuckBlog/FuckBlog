# -*- coding: utf-8 -*-
# 2017/1/4 10:32
"""
-------------------------------------------------------------------------------
Function:   a small simple of our web app
Version:    1.0
Author:     SLY
Contact:    slysly759@gmail.com 
 
-------------------------------------------------------------------------------
"""

import logging
logging.basicConfig(level=logging.INFO)
import asyncio, json, os, time
from datetime import datetime
from aiohttp import web
# 首要解决的就是这个parse函数自解析
from urllib import parse
import www.orm
from www.webframe import add_routes, add_static
from jinja2 import Environment, FileSystemLoader
from www.login_data_transfer import auth_factory
def init_jinjia2(app, **kw):
    logging.info('init jinja2 template...')
    options=dict(
        autoescape = kw.get('autoescape', True),
        block_start_string = kw.get('block_start_string','{%',),
        block_end_string=kw.get('block_end_string','%}'),
        variable_start_string=kw.get('variable_start_string','{{'),
        variable_end_string=kw.get('variable_end_string','}}'),
        auto_reload=kw.get('auto_reload', True)
    )
    path=kw.get('path',None)
    if path is None:
        # 以下代码如果只是将路径指向templates的绝对路径的话 作者你过来我保证不打死你
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'templates')
        logging.info('The jinjia template is set here: %s'% path)
        env = Environment(loader=FileSystemLoader(path), **options)
        filters=kw.get('filters', None)
        if filters is not None:
            for name, f in filters.items():
                env.filters[name]=f
        app['__templating__']= env
# 老子就是爱用coroutine装饰 你咬我啊
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
            print(content_type)
            if content_type.startswith('application/json'):
                request.__data__= yield from request.json()
                if not isinstance(request.__data__, dict):
                    return web.HTTPBadRequest(text='must be a json object')

                logging.info('request json %s ' %str(request.__data__))
            elif request.content_type.startswith('application/x-www-form-urlencoded'):
                params =yield from  request.post()
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
        if isinstance(r,bytes):
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


@asyncio.coroutine
def fuck_init(loop):
    yield from www.orm.create_pool(loop=loop,host='localhost', port=3308, user='sly', password='070801382',db='fuckblog')
    app = web.Application(loop=loop, middlewares=[
        logger_factory, response_factory, data_factory, auth_factory
    ])
    init_jinjia2(app, filters=dict(datetime=datetime_filter))
    add_routes(app,'handlers')
    add_static(app)
    srv=yield from loop.create_server(app.make_handler(),'127.0.0.1',9000)
    logging.info('server is starting at 9000 port')
    return srv
loop = asyncio.get_event_loop()
loop.run_until_complete(fuck_init(loop))
loop.run_forever()
