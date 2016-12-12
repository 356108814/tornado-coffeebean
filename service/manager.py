# encoding: utf-8
"""
服务管理器
@author Yuriseus
@create 2016-12-10 23:15
"""
from .user import UserService


class ServiceManger(object):
    def __init__(self):
        self.user = UserService()


service_manger = ServiceManger()
