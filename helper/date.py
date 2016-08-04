# encoding: utf-8
"""
日期辅助类
@author Yuriseus
@create 2016-8-4 19:26
"""
import time


class DateHelper(object):

    @staticmethod
    def date2timestamp(date_str, fmt='%Y-%m-%d'):
        time_array = time.strptime(date_str, fmt)
        timestamp = int(time.mktime(time_array))
        return timestamp

    @staticmethod
    def timestamp2date(timestamp, fmt='%Y-%m-%d'):
        time_array = time.localtime(timestamp)
        return time.strftime(fmt, time_array)
