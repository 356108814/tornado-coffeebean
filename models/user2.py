# encoding: utf-8
"""
用户
@author Yuriseus
@create 2016-12-10 21:21
"""
from .base import BaseModel


class User(BaseModel):

    def __init__(self):
        self.id = 0
        self.username = ''
        self.password = ''
        self.real_name = ''
        self.status = 1
        self.cellphone = ''
        self.email = ''


