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
from www.webframe.factory import logger_factory,data_factory,response_factory, auth_factory
import www.webframe.orm
from www.base import add_routes, add_static
from jinja2 import Environment, FileSystemLoader

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
    yield from www.webframe.orm.create_pool(loop=loop,host='localhost', port=3308, user='sly', password='070801382',db='fuckblog')
    app = web.Application(loop=loop, middlewares=[
        logger_factory, response_factory, data_factory,
    ])
    init_jinjia2(app, filters=dict(datetime=datetime_filter))
    add_routes(app,'api')
    add_static(app)
    srv=yield from loop.create_server(app.make_handler(),'127.0.0.1',9000)
    logging.info('server is starting at 9000 port')
    return srv
loop = asyncio.get_event_loop()
loop.run_until_complete(fuck_init(loop))
loop.run_forever()
