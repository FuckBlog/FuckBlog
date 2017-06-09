# -*- coding: utf-8 -*-
# 2017/1/10 15:49
"""
-------------------------------------------------------------------------------
Function:   程序运行的配置文件哈哈哈哈
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

import config.congfig_default
# 下面新建一个字典方法用于让其指出a.b的特性
# 对了我对于用py来存储dict 而不是ini文件也是很醉的
# 注意 日后我需要你仿造wp 首先本地假设服务 然后输入数据库的配置信息写入config_default的设置

class Dict(dict):
    def __init__(self, names=(), values=(), **kw):
        super(Dict,self).__init__(**kw)
        for k,v in zip(names, values):
            self[k]=v
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError('Dict object has no attribute %s'%key)
    def __setattr__(self, key, value):
        self[key]=value

def _merge(defaults,override):
    r={}
    for k,v in defaults.items():
        if k in override:
            # 如果判断字典键值重复而且仍然是一个字典就扔进这个函数
            if isinstance(v,dict):
                r[k]=_merge(v,override[k])
            else:
                r[k]=override[k]
        else:
            r[k]=v
    return r

def to_Dict(d):
    D=Dict()
    for k, v in d.items():
        # 注意 他需要将字典里的字典也要拥有该a.b的属性因此又扔进去了
        D[k]=to_Dict(v) if isinstance(v,dict) else v
    return D
configs=config.congfig_default.configs

try:
    import config.config_override
    configs=_merge(configs, config.config_override.configs)
except:
    pass
# 保证传递过来的dict全是拥有a.b特性的东西
configs = to_Dict(configs)


