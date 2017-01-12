# -*- coding: utf-8 -*-
# 2017/1/7 19:29
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
# import asyncio,sys
# from www import orm
# from www.models import User, Blog, Comment
# if __name__=="__main__":
#     loop = asyncio.get_event_loop()
#     @asyncio.coroutine
#     def test():
#
#         yield from orm.create_pool(loop=loop,host='localhost', port=3308, user='sly', password='070**382', db='fuckblog')
#         u = User(name='sly', email='slysly759@gmail.com', password='1234567890', image='about:blank',admin_flag=True)
#
#         yield from u.save()
#         yield from orm.destroy_pool()
#
#     loop.run_until_complete(test())
#     loop.close()
#     if loop.is_closed():
#         sys.exit(0)

import asyncio

loop = asyncio.get_event_loop()


@asyncio.coroutine
def handler():
    print('Before Sleep')
    yield from asyncio.sleep(1)
    print('After Sleep')
    return 1


async def run():
    print('Run started')
    res = await handler()
    assert res == 1, res
    print('Run ended')
    loop.stop()

loop.run_until_complete(asyncio.ensure_future(run()))
loop.run_forever()
