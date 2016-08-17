# encoding: utf-8
"""

@author Yuriseus
@create 2016-8-4 14:21
"""
from sqlalchemy import Integer, Column, String, DateTime

from coffeebean.db import BaseModel


class User(BaseModel):
    __tablename__ = 'user'

    id = Column(Integer(), primary_key=True)
    name = Column(String(32))
    age = Column(Integer())
    birth = Column(DateTime(), nullable=True)

    @classmethod
    def get_table_name(cls, column_value):
        index = column_value['id'] % 64
        return 'user_%s' % index
