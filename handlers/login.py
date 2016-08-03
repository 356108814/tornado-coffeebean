# encoding: utf-8
"""
登陆
@author Yuriseus
@create 2016-8-3 11:42
"""
from .base import BaseHandler


class LoginHandler(BaseHandler):
    def get(self):
        name = self.get_argument('name', None)
        if name:
            self.session['user'] = name
            self.redirect('/')
        else:
            self.finish('请登陆')
