# encoding: utf-8
"""
应用总配置
@author Yuriseus
@create 2016-8-1 14:12
"""

import tornado.web
from tornado.util import import_object

import settings
from coffeebean.session import SessionManager
from urls import handlers


class Application(tornado.web.Application):

    def __init__(self):
        __settings = {
            'debug': settings.DEBUG,
            'static_path': settings.STATIC_PATH,
            'template_path': settings.TEMPLATE_PATH,
            'cookie_secret': 'LT4gKTS6nzTg'
        }
        super(Application, self).__init__(handlers=handlers, **__settings)

        # 初始化session管理
        self.session_manager = SessionManager()

        # 加载拦截器
        self.interceptor_intercept = None
        self.load_interceptor()

    def load_interceptor(self):
        self.interceptor_intercept = []
        for interceptor_path in settings.INTERCEPTOR_CLASSES:
            ic_class = import_object(interceptor_path)
            ic = ic_class()
            if hasattr(ic, 'intercept'):
                self.interceptor_intercept.append(ic.intercept)






