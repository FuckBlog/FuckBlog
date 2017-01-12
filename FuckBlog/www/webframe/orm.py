# -*- coding: utf-8 -*-
# 2017/1/4 11:02
"""
-------------------------------------------------------------------------------
Function:   封装的ORM工具类
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
import sys
import asyncio
import logging
logging.basicConfig(level=logging.INFO)
# 一次使用异步 处处使用异步
import aiomysql

def log(sql,args=()):
    logging.info('SQL:%s :%s' %(sql, args))
'''
警告：
async替代python3.4中的@asyncio.coroutine，用await替代yield from
本orm采用为3.4写法，想用更高级写法亦可。除了执行更加清晰以外，效率略低，具体低的原因不明。
'''
@asyncio.coroutine
def create_pool(loop, **kw):
    logging.info(' start creating database connection pool')
    global __pool
    # 理解这里的yield from 是很重要的
    __pool= yield from aiomysql.create_pool(
        host=kw.get('host', 'localhost'),
        port=kw.get('port', 3306),
        user=kw['user'],
        password=kw['password'],
        db=kw['db'],
        charset=kw.get('charset','utf8'),
        autocommit=kw.get('autocommit', True),
        # 最高携程支持10 个同时连接 最小1
        maxsize=kw.get('maxsize', 10),
        minsize=kw.get('minsize', 1),
        loop=loop
        )

@asyncio.coroutine
def destroy_pool():
    global __pool
    if __pool is not None :
        __pool.close()
        yield from __pool.wait_closed()

# 我很好奇为啥不用commit 事务不用提交么
@asyncio.coroutine
def select(sql, args, size=None):
    log(sql,args)
    global __pool
    # 666 建立游标
    # -*- yield from 将会调用一个子协程，并直接返回调用的结果
    # yield from从连接池中返回一个连接
    with (yield from __pool) as conn:
        cur = yield from conn.cursor(aiomysql.DictCursor)
        yield from cur.execute(sql.replace('?', '%s'), args)# 将Python %s 占位符替换为sql语言的
        if size:
            rs = yield from cur.fetchmany(size)# 获取指定行数
        else:
            rs = yield from cur.fetchall()
        yield from cur.close()
        logging.info('rows have returned %s' %len(rs))
    return rs


# 封装INSERT, UPDATE, DELETE
# 语句操作参数一样，所以定义一个通用的执行函数
# 返回操作影响的行号

@asyncio.coroutine
def execute(sql,args, autocommit=True):
    log(sql)
    global __pool
    with (yield from __pool) as conn:
        try:
            # 因为execute类型sql操作返回结果只有行号，不需要dict
            cur = yield from conn.cursor()
            # 顺便说一下 后面的args 别掉了 掉了是无论如何都插入不了数据的
            yield from cur.execute(sql.replace('?', '%s'), args)
            yield from conn.commit()
            affected_line=cur.rowcount
            yield from cur.close()
            print('execute : ', affected_line)
        except BaseException as e:
            raise

        return affected_line

# 这个函数主要是把查询字段计数 替换成sql识别的?
# 比如说：insert into  `User` (`password`, `email`, `name`, `id`) values (?,?,?,?)  看到了么 后面这四个问号
def create_args_string(num):
    lol=[]
    for n in range(num):
        lol.append('?')
    return (','.join(lol))

# 定义Field类，负责保存(数据库)表的字段名和字段类型
class Field(object):
    # 表的字段包含名字、类型、是否为表的主键和默认值
    def __init__(self, name, column_type, primary__key, default):
        self.name = name
        self.column_type=column_type
        self.primary_key=primary__key
        self.default=default
    def __str__(self):
        # 返回 表名字 字段名 和字段类型
        return "<%s , %s , %s>" %(self.__class__.__name__, self.name, self.column_type)
# 定义数据库中五个存储类型
class StringField(Field):
    def __init__(self, name=None, primary_key=False, default=None, ddl='varchar(100)'):
        super().__init__(name,ddl,primary_key,default)
# 布尔类型不可以作为主键
class BooleanField(Field):
    def __init__(self, name=None, default=None):
        super().__init__(name,'Boolean',False, default)
# 不知道这个column type是否可以自己定义 先自己定义看一下
class IntegerField(Field):
    def __init__(self, name=None, primary_key=False, default=0):
        super().__init__(name, 'int', primary_key, default)
class FloatField(Field):
    def __init__(self, name=None, primary_key=False,default=0.0):
        super().__init__(name, 'float', primary_key, default)
class TextField(Field):
    def __init__(self, name=None, default=None):
        super().__init__(name,'text',False, default)
# class Model(dict,metaclass=ModelMetaclass):

# -*-定义Model的元类

# 所有的元类都继承自type
# ModelMetaclass元类定义了所有Model基类(继承ModelMetaclass)的子类实现的操作

# -*-ModelMetaclass的工作主要是为一个数据库表映射成一个封装的类做准备：
# ***读取具体子类(user)的映射信息
# 创造类的时候，排除对Model类的修改
# 在当前类中查找所有的类属性(attrs)，如果找到Field属性，就将其保存到__mappings__的dict中，同时从类属性中删除Field(防止实例属性遮住类的同名属性)
# 将数据库表名保存到__table__中

# 完成这些工作就可以在Model中定义各种数据库的操作方法
# metaclass是类的模板，所以必须从`type`类型派生：

# ModelMetaclass这是一个元类，它定义了如何来构造一个类，任何定义了__metaclass__属性或指定了metaclass的都会通过元类定义的构造方法构造类
# 任何继承自Model的类，都会自动通过ModelMetaclass扫描映射关系，并存储到自身的类属性
class ModelMetaclass(type):
    # __new__控制__init__的执行，所以在其执行之前
    # cls:代表要__init__的类，此参数在实例化时由Python解释器自动提供(例如下文的User和Model)
    # bases：代表继承父类的集合
    # attrs：类的方法集合
    def __new__(cls, name, bases, attrs):
        # 排除model 是因为要排除对model类的修改
        if name=='Model':
            return type.__new__(cls, name, bases, attrs)
                # cls: 当前准备创建的类对象,相当于self
        # name: 类名,比如User继承自Model,当使用该元类创建User类时,name=User
        # bases: 父类的元组
        # attrs: 属性(方法)的字典,比如User有__table__,id,等,就作为attrs的keys
        # 排除Model类本身,因为Model类主要就是用来被继承的,其不存在与数据库表的映射
        table_name=attrs.get('__table__', None) or name
        logging.info('found table: %s (table: %s) ' %(name,table_name ))
        # 获取Field所有主键名和Field

        mappings=dict()# 用于保存映射关系
        fields=[] # 保存所有字段名
        primaryKey=None # 保存主键
        # 这个k是表示字段名
        for k, v in attrs.items():
            if isinstance(v, Field):
                logging.info('Found mapping %s===>%s' %(k, v))
            # 注意mapping的用法
                mappings[k] = v
                if v.primary_key:
                    logging.info('fond primary key hahaha %s'%k)
                    # 这里很有意思 当第一次主键存在primaryKey被赋值 后来如果再出现主键的话就会引发错误
                    if primaryKey:
                        raise RuntimeError('Duplicated key for field')
                    primaryKey=k
                else:
                    fields.append(k)

        if not primaryKey:
            raise RuntimeError('Primary key not found!')
        # w下面位字段从类属性中删除Field 属性
        for k in mappings.keys():
            attrs.pop(k)

        # 保存除主键外的属性为''列表形式
        # 这一句的lambda表达式没懂
        escaped_fields=list(map(lambda f:'`%s`' %f, fields))
        # 保存属性和列的映射关系
        attrs['__mappings__']=mappings
        # 保存表名
        attrs['__table__']=table_name
        # 保存主键名称
        attrs['__primary_key__']=primaryKey
        # 保存主键外的属性名
        attrs['__fields__']=fields
        # 构造默认的增删改查 语句
        attrs['__select__']='select `%s`, %s from `%s` '%(primaryKey,', '.join(escaped_fields), table_name)
        attrs['__insert__'] = 'insert into  `%s` (%s, `%s`) values (%s) ' %(table_name, ', '.join(escaped_fields), primaryKey, create_args_string(len(escaped_fields)+1))
        attrs['__update__']='update `%s` set %s where `%s` = ?' %(table_name, ', '.join(map(lambda f:'`%s`=?' % (mappings.get(f).name or f), fields)), primaryKey)
        attrs['__delete__']='delete `%s` where `%s`=?' %(table_name, primaryKey)
        return type.__new__(cls, name, bases, attrs)


# 定义ORM所有映射的基类：Model
# Model类的任意子类可以映射一个数据库表
# Model类可以看作是对所有数据库表操作的基本定义的映射


# 基于字典查询形式
# Model从dict继承，拥有字典的所有功能，同时实现特殊方法__getattr__和__setattr__，能够实现属性操作
# 实现数据库操作的所有方法，定义为class方法，所有继承自Model都具有数据库操作方法

class Model(dict,metaclass=ModelMetaclass):
    def __init__(self, **kw):
        super(Model,self).__init__(**kw)
    # 增加__getattr__方法，使获取属性更加简单，即可通过"a.b"的形式
    # __getattr__ 当调用不存在的属性时，python解释器会试图调用__getattr__(self, 'attr')来尝试获得属性
    # 例如b属性不存在，当调用a.b时python会试图调用__getattr__(self, 'b')来获得属性，在这里返回的是a[b]对应的值
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError("'Model' object have no attribution: %s"% key)
    # 增加__setattr__方法，使设置属性更方便，可通过"a.b=c"的形式
    def __setattr__(self, key, value):
        self[key] = value
    def getValue(self, key):
        # 这个是默认内置函数实现的
        return getattr(self, key, None)

    def getValueOrDefault(self, key):
        value=getattr(self, key , None)
        if value is None:
            field = self.__mappings__[key]
            if field.default is not None:
                value = field.default() if callable(field.default) else field.default
                logging.info('using default value for %s : %s ' % (key, str(value)))
                setattr(self, key, value)

        return value
    # classmethod装饰器将方法定义为类方法
    # 对于查询相关的操作，我们都定义为类方法，就可以方便查询，而不必先创建实例再查询
    # 查找所有合乎条件的信息
    @classmethod
    # 类方法有类变量cls传入，从而可以用cls做一些相关的处理。并且有子类继承时，调用该类方法时，传入的类变量cls是子类，而非父类。
    @asyncio.coroutine

    def find_all(cls, where=None, args=None, **kw):
        sql = [cls.__select__]
        if where:
            sql.append('where')
            sql.append(where)
        if args is None:
            args = []

        orderBy = kw.get('orderBy', None)
        if orderBy:
            sql.append('order by')
            sql.append(orderBy)
        # dict 提供get方法 指定放不存在时候返回后学的东西 比如a.get('Fuck',None)
        limit = kw.get('limit', None)
        if limit is not None:
            sql.append('limit')
            if isinstance(limit, int):
                sql.append('?')
                args.append(limit)
            elif isinstance(limit, tuple) and len(limit) ==2:
                sql.append('?,?')
                args.extend(limit)
            else:
                raise ValueError('Invalid limit value : %s '%str(limit))

        rs = yield from select(' '.join(sql),args)
        return [cls(**r) for r in rs]
    @classmethod
    @asyncio.coroutine
    def findNumber(cls, selectField, where=None, args=None):
        '''find number by select and where.'''
        sql = ['select %s __num__ from `%s`' %(selectField, cls.__table__)]
        if where:
            sql.append('where')
            sql.append(where)
        rs = yield from select(' '.join(sql), args, 1)
        if len(rs) == 0:
            return None
        return rs[0]['__num__']

    # 这个黑魔法我还在研究呢~
    @classmethod
    @asyncio.coroutine
    def find(cls, primarykey):
        '''find object by primary key'''
        rs = yield from select('%s where `%s`=?' %(cls.__select__, cls.__primary_key__), [primarykey], 1)
        if len(rs) == 0:
            return None
        return cls(**rs[0])

    @asyncio.coroutine
    def save(self):
        args = list(map(self.getValueOrDefault, self.__fields__))
        print('save:%s' % args)
        args.append(self.getValueOrDefault(self.__primary_key__))
        rows = yield from execute(self.__insert__, args)
        if rows != 1:
            print(self.__insert__)
            logging.warning('failed to insert record: affected rows: %s' %rows)

    @asyncio.coroutine
    # 显示方言错误是什么鬼。。。
    def update(self):
        args = list(map(self.getValue, self.__fields__))
        args.append(self.getValue(self.__primary_key__))
        rows = yield from execute(self.__update__, args)
        if rows != 1:
            logging.warning('failed to update record: affected rows: %s'%rows)

    @asyncio.coroutine
    def remove(self):
        args = [self.getValue(self.__primary_key__)]
        rows = yield from execute(self.__updata__, args)
        if rows != 1:
            logging.warning('failed to remove by primary key: affected rows: %s' %rows)

'''
以下代码 仅供测试使用
if __name__=="__main__":
    class User(Model):
        id = IntegerField('id',primary_key=True)
        name = StringField('username')
        email = StringField('email')
        password = StringField('password')
    #创建异步事件的句柄
    loop = asyncio.get_event_loop()

    #创建实例
    @asyncio.coroutine
    def test():
        yield from create_pool(loop=loop,host='localhost', port=3308, user='sly', password='070801382', db='test')
        user = User(id=8, name='sly', email='slysly759@gmail.com', password='fuckblog')
        yield from user.save()
        r = yield from User.find('11')
        print(r)
        r = yield from User.find_all()
        print(1, r)
        r = yield from User.find_all(id='12')
        print(2, r)
        yield from destroy_pool()

    loop.run_until_complete(test())
    loop.close()
    if loop.is_closed():
        sys.exit(0)

'''