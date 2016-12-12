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
        pagination = service.get_users()
        users = pagination.items
        print(users)
        self.finish('Hello %s' % self.session['user'])

