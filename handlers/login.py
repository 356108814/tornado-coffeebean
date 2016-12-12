# encoding: utf-8
"""
登陆
@author Yuriseus
@create 2016-8-3 11:42
"""
from tornado.web import RequestHandler

from coffeebean.decorators import valid
from service.manager import service_manger

from .base import BaseHandler
from .response_code import ResponseCode

service = service_manger.user


class LoginHandler(BaseHandler):

    def get(self):
        self.render('login.html')

    @valid(cfg={'username': {'type': 'string', 'required': True},
                'password': {'type': 'string', 'required': True}})
    def post(self):
        username = self.get_argument('username', '')
        password = self.get_argument('password', '')
        # 记住我
        online = self.get_argument('online', '')
        user = service.get_user_by_login(username, password)
        if user:
            self.session['user'] = user
            if online == 'on':
                self.set_cookie('username', username)
                self.set_cookie('password', password)
            else:
                self.clear_cookie('username')
                self.clear_cookie('password')
            self.write_response()
        else:
            self.write_response(response_code=ResponseCode.USER_VALID_ERROR)


class LogoutHandler(BaseHandler):

    def get(self):
        self.session['user'] = None
        self.redirect('/login')
