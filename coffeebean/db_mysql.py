# coding:utf-8
from queue import Queue

import pymysql


class DBMySQL(object):
    """
    数据库操作基类
    """
    def __init__(self, host, port, user, password, db):
        self.pool_size = 10
        self._pool = Queue(maxsize=self.pool_size)
        self._host = host
        self._port = int(port)
        self._user = user
        self._password = password
        self._db = db

        self._connection = None
        self.init_pool(self.pool_size)

    def init_pool(self, pool_size):
        for x in range(pool_size):
            self._pool.put_nowait(self.create_connection())

    def create_connection(self):
        connection = pymysql.connect(host=self._host,
                                     port=self._port,
                                     user=self._user,
                                     password=self._password,
                                     db=self._db,
                                     autocommit=False,
                                     charset='utf8',
                                     cursorclass=pymysql.cursors.DictCursor)
        return connection

    @property
    def connection(self):
        self._connection = self._pool.get(True)
        if not self.ping():
            self._connection.connect()
        return self._connection

    def ping(self):
        try:
            return self._connection.query('SELECT 1')
        except Exception:
            return None

    def query(self, sql, params_dict=None, is_fetchone=False):
        """
        执行sql查询语句。如：select * from user where name = '{name}'
        @param sql sql语句
        @param params_dict 参数字典
        @param is_fetchone 是否只返回一条记录
        @return dict列表或dict
        """
        result = None
        with self.connection.cursor() as cursor:
            # sql格式化
            if params_dict:
                for (key, value) in params_dict.items():
                    sql = sql.replace('{%s}' % key, value)
            try:
                cursor.execute(sql)
            except Exception as e:
                raise e
            if is_fetchone:
                result = cursor.fetchone()
            else:
                result = cursor.fetchall()
        return result

    def execute(self, sql, params_dict=None):
        """
        执行sql语句
        @param sql:
        @param params_dict:
        @return:
        """
        is_success = False
        connection = self.connection
        with connection.cursor() as cursor:
            # sql格式化
            if params_dict:
                for (key, value) in params_dict.items():
                    sql = sql.replace('{%s}' % key, value)
            try:
                cursor.execute(sql)
                is_success = True
            except Exception as e:
                raise e
        connection.commit()
        return is_success

    def close(self):
        # if self.connection:
        #     self.connection.close()
        while not self._pool.empty():
            self._pool.get(True).close()


if __name__ == '__main__':
    pass
    # dbMySQL = DBMySQL(host='172.16.30.6', port=3306, user='minik_act', password='cvcRixego3Ju2bi+', db='minikinvestment')
    # sql = 'select * from applicant'
    # result = dbMySQL.query(sql)
    # print(result)
