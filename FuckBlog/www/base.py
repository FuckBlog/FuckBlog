# -*- coding: utf-8 -*-
# 2017/1/8 10:35
"""
-------------------------------------------------------------------------------
Function:   deal request from web user
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


import asyncio,os, logging
'''
inspect 库提供一下四种功能

(1).对是否是模块，框架，函数等进行类型检查。

(2).获取源码

(3).获取类或函数的参数的信息

(4).解析堆栈
'''
import inspect
import functools
# 利用工厂模式，生成GET POST 等方法请求装饰器
from aiohttp import web
from www.errors import APIError

def request(path, *, method):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args,**kw):
            return func(*args, **kw)
        wrapper.__method__ = method
        wrapper.__route__ = path
        return wrapper
    return decorator
# 下面这个用的是廖雪峰讲过的偏函数 指定传入一个参数为固定值。

get = functools.partial(request, method='GET')
post = functools.partial(request, method='POST')
put = functools.partial(request, method='PUT')
delete = functools.partial(request, method='DELETE')

# 不得不说 比廖雪峰给的样板例子强太多 墨灵这位仁兄的确是掌握了Python大部分基础知识能够举一反三。

class RequestHandler(object):  # 初始化一个请求处理类

    def __init__(self, func):
        self._func = asyncio.coroutine(func)

    async def __call__(self, request):  # 任何类，只需要定义一个__call__()方法，就可以直接对实例进行调用
        # 获取函数的参数表
        required_args = inspect.signature(self._func).parameters
        logging.info('required args: %s' % required_args)

        # 获取从GET或POST传进来的参数值，如果函数参数表有这参数名就加入
        kw = {arg: value for arg, value in request.__data__.items() if arg in required_args}
        print(dir(kw))
        # 获取match_info的参数值，例如@get('/blog/{id}')之类的参数值
        kw.update(request.match_info)

        # 如果有request参数的话也加入
        if 'request' in required_args:
            kw['request'] = request

        # 检查参数表中有没参数缺失
        for key, arg in required_args.items():
            # request参数不能为可变长参数
            if key == 'request' and arg.kind in (arg.VAR_POSITIONAL, arg.VAR_KEYWORD):
                return web.HTTPBadRequest(text='request parameter cannot be the var argument.')
            # 如果参数类型不是变长列表和变长字典，变长参数是可缺省的
            if arg.kind not in (arg.VAR_POSITIONAL, arg.VAR_KEYWORD):
                # 如果还是没有默认值，而且还没有传值的话就报错
                if arg.default == arg.empty and arg.name not in kw:
                    return web.HTTPBadRequest(text='Missing argument: %s' % arg.name)

        logging.info('call with args: %s' % kw)
        try:
            return await self._func(**kw)
        except APIError as e:
            return dict(error=e.error, data=e.data, message=e.message)

def add_static(app):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
    app.router.add_static('/static/', path)
    logging.info('add static %s ==> %s' %('/static/', path))

def add_routes(app, module_name):
    try:
        mod = __import__(module_name, fromlist=['get_submodule'])
    except ImportError as e:
        raise e
    # 遍历mod的方法和属性,主要是找处理方法
    # 由于我们定义的处理方法，被@get或@post修饰过，所以方法里会有'__method__'和'__route__'属性

    for attr in dir(mod):
        # 如果是以'_'开头的，一律pass，我们定义的处理方法不是以'_'开头的
        if attr.startswith('_'):
            continue
        # 获取到非'_'开头的属性或方法
        func = getattr(mod, attr)
        # 获取有__method___和__route__属性的方法
        # 娘希匹的终于搞定这个不能加载的问题了  这里注意 ResquestHandler 一定不能用@asyncore装饰调用携程
        if callable(func) and hasattr(func, '__method__') and hasattr(func, '__route__'):
            args = ', '.join(inspect.signature(func).parameters.keys())
            logging.info('add route %s %s => %s(%s)' % (func.__method__, func.__route__, func.__name__, args))
            app.router.add_route(func.__method__, func.__route__, RequestHandler(func))
        #     print('sucess')
        # else:
        #     print('不能加载动态路由表')

class Page():
    # 参数分别是          文章总数    当前页  一页显示文章数量
    def __init__(self,article_count, index=1, page_size=10):
        # 文章数量是有可能为零的 做一下备注
        if article_count>0:
            self.last_page=article_count // page_size +(1 if article_count % page_size >0 else 0)# 记录最后一页 你可以理解为总页数
            self.index=index  # 当前页
            self.offset=page_size*(index-1) # 已经显示了多少文章，用于数据库查询偏移
            self.limit=page_size
        else:
            self.last_page=1
            self.article_count=0
            self.index=1
            self.offset=0
            self.limit=10
    def __str__(self):
        # 重写显示 为了方便我们调试
        return  ' last_page: %s, index: %s, page_size: %s, offset: %s, limit: %s' % ( self.last_page, self.index, self.limit, self.offset, self.limit)
    __repr__=__str__
