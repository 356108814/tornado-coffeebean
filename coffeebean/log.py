# encoding: utf-8
"""
增加多文件日志支持
@author Yuriseus
@create 2016-8-3 19:15
"""
import logging
import logging.handlers
from tornado.log import LogFormatter
from tornado.log import gen_log


def gen_channel(filename):
    return logging.handlers.TimedRotatingFileHandler(
            filename='log/%s.log' % filename,
            when='midnight',
            interval=1,
            backupCount=3)


class Logger(object):

    def __init__(self):
        self._loggers = {}

    def info(self, msg, name=None):
        """
        记录日志
        :param msg:
        :param name: 日志文件名称，如不存在，则创建
        :return:
        """
        if name:
            if name not in self._loggers:
                temp_logger = logging.getLogger(name)
                channel = gen_channel(name)
                channel.setFormatter(LogFormatter(color=True))
                temp_logger.addHandler(channel)
                self._loggers[name] = temp_logger
            current_logger = self._loggers[name]
            current_logger.info(msg)
        else:
            gen_log.info(msg)


logger = Logger()
