# encoding: utf-8
"""
用户
@author Yuriseus
@create 2016-8-5 17:32
"""
# from .base import BaseService
from .base_mysql import BaseService


class UserService(BaseService):

    def __init__(self):
        super().__init__('user')

    def get_user_by_login(self, username, password):
        """
        根据登陆信息获取用户
        @param username:
        @param password:
        @return: 成功返回dict,失败返回None
        """
        sql = "SELECT * FROM " + self.table_name + " WHERE username = %(username)s"
        params_dict = {'username': username, 'table_name': self.table_name}
        row = self.db.query(sql, params_dict, True)
        if row:
            db_password = row['password']
            if db_password and db_password == password:
                return row
        return None



