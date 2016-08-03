# encoding: utf-8
"""
默认处理器
@author Yuriseus
@create 2016-8-1 15:20
"""
from tornado.web import RequestHandler
from .session import Session
from .log import logger


class BaseRequestHandler(RequestHandler):
    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)
        self.session = Session(self.application.session_manager, self)
        self.logger = logger

    def initialize(self):
        pass

    def prepare(self):
        for interceptor_method in self.application.interceptor_intercept:
            return_value = interceptor_method(self)
            if return_value:    # 拦截器有返回值，终止后续的拦截器
                break

    def on_finish(self):
        pass



