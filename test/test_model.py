# encoding: utf-8
"""

@author Yuriseus
@create 2016-8-4 11:15
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer(), primary_key=True)
    name = Column(String(32))
    age = Column(Integer())
