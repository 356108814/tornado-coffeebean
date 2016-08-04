# encoding: utf-8
"""
缓存
@author Yuriseus
@create 2016-8-1 14:42
"""
import redis
import settings


class Cache(object):
    def __init__(self):
        conf = settings.CONF['cache']
        self._redis = redis.StrictRedis(host=conf['host'], port=conf['port'], db=conf['db'])

    def get_redis(self):
        return self._redis

cache = Cache().get_redis()
