# encoding: utf-8
"""
db数据库操作模块。默认pymysql+sqlalchemy
@author Yuriseus
@create 2016-8-4 14:03
"""

from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta, declared_attr
from sqlalchemy.orm import scoped_session, sessionmaker, Query
import settings


class ModelMeta(DeclarativeMeta):
    def __new__(cls, name, bases, d):
        column_name_sets = set()
        for k, v in d.items():
            if getattr(v, '__class__', None) is None:
                continue
            if v.__class__.__name__ == 'Column':
                column_name_sets.add(k)

        # obj = type.__new__(cls, name, bases, dict(namespace))
        instance = super(ModelMeta, cls).__new__(cls, name, bases, dict(d))
        instance._column_name_sets = column_name_sets
        return instance

__Base = declarative_base(metaclass=ModelMeta)


class BaseModel(__Base):
    __abstract__ = True

    # 基类的 _column_name_sets  是为实现的类型
    _column_name_sets = NotImplemented

    def to_dict(self):
        return dict(
            (column_name, getattr(self, column_name, None)) for column_name in self._column_name_sets
        )

    @classmethod
    def get_column_name_sets(cls):
        """
        获取 column 的定义的名称(不一定和数据库字段一样)
        """
        return cls._column_name_sets

    @declared_attr
    def Q(cls):
        return SQLAlchemy.instance().query()

    @declared_attr
    def session(cls):
        return SQLAlchemy.instance().session

    @declared_attr
    def connect(cls):
        return SQLAlchemy.instance().connect

    @classmethod
    def execute_query(cls, sql, param_dict):
        stmt = text(sql)
        if param_dict and isinstance(param_dict, dict):
            stmt = stmt.bindparams(**param_dict)
        records = []
        row_proxys = cls.connect.execute(stmt).fetchall()
        for _, row in enumerate(row_proxys):
            one = {}
            for i, t in enumerate(row.items()):
                one[t[0]] = t[1]
            records.append(one)
        return records

    @classmethod
    def execute_update(cls, sql, param_dict):
        stmt = text(sql)
        if param_dict and isinstance(param_dict, dict):
            stmt = stmt.bindparams(**param_dict)
        result_proxy = cls.connect.execute(stmt)
        return result_proxy.lastrowid

    def __str__(self):
        return str(self.to_dict())

    def __repr__(self):
        return str(self.to_dict())


class SQLAlchemy(object):

    def __init__(self, host, port, user, password, db, **kwargs):
        param = {'host': host, 'port': port, 'user': user, 'password': password, 'db': db}
        self._db_url = 'mysql+pymysql://{user}:{password}@{host}:{port}/{db}'.format(**param)
        self._session = None
        self._connect = None

    @staticmethod
    def instance():
        if not hasattr(SQLAlchemy, "_instance"):
            conf = settings.CONF['db']
            SQLAlchemy._instance = SQLAlchemy(conf['host'], conf['port'], conf['user'], conf['password'], conf['db'])
        return SQLAlchemy._instance

    @property
    def session(self):
        if not self._session:
            self._session = self.create_session(self._db_url)
        return self._session

    @property
    def connect(self):
        if not self._connect:
            engine = create_engine(self._db_url, echo=False)
            self._connect = engine.connect()
        return self._connect

    def query(self):
        return self.session.query_property(Query)    # 查询出模型属性值

    @staticmethod
    def create_session(db_url, **kwargs):
        engine = create_engine(db_url, echo=True)
        session = sessionmaker(autocommit=False, **kwargs)    # 默认关闭事务
        session.configure(bind=engine)
        return scoped_session(session)

    def remove(self):
        if self._session:
            self._session.remove()

# conf = settings.CONF['db']
# sqlalchemy = SQLAlchemy(conf['host'], conf['port'], conf['user'], conf['password'], conf['db'])

if __name__ == '__main__':
    from models.user import User
    # l = User.session.query(User).all()
    # sql = 'select * from user where name= :name'
    # l = User.execute_query(sql, {'name': 'yuri'})
    sql = 'INSERT INTO user (name, age) VALUES (:name, :age)'
    l = User.execute_update(sql, {'name': 'hh', 'age': 22})

