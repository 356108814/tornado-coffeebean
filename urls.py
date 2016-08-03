# encoding: utf-8
"""
url路由配置
@author Yuriseus
@create 2016-8-3 14:36
"""
from tornado.web import StaticFileHandler

from handlers.index import IndexHandler
from handlers.login import LoginHandler
import settings

handlers = [
    (r'/?', IndexHandler),
    (r'/login/?', LoginHandler),

    (r"/(favicon\.ico)", StaticFileHandler, dict(path=settings.STATIC_PATH)),
]
