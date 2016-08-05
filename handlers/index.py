# encoding: utf-8
"""
首页
@author Yuriseus
@create 2016-8-1 18:09
"""
from service.user import UserService
from .base import BaseHandler

service = UserService()


class IndexHandler(BaseHandler):
    def get(self):
        users = service.get_users()
        print(users)
        self.finish('Hello %s' % self.session['user'])
        pass
