# encoding: utf-8
"""
基础业务类
@author Yuriseus
@create 2016-8-3 20:10
"""
from coffeebean.log import logger
from coffeebean.cache import Cache


class BaseService(object):
    def __init__(self):
        self.logger = logger
        self.cache = Cache.current()

