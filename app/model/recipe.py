from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import MetaData
from sqlalchemy import Table

from datetime import datetime


__all__ = ('user', 'recipe')

meta = MetaData()

recipe = Table(
    "recipe", meta,

    Column('recipe_id', Integer, primary_key=True),
    Column('author', Integer, ForeignKey('users.user_id')),
    Column('datetime', DateTime, default=datetime.now()),
    Column('recipe_name', String),
    Column('info', String),
    Column('cooking_steps', String),
    Column('photo', ),  # ???????????????????????????
    Column('food_type', String),
    Column('likes_count', Integer, default=0),
    Column('hashtag_set', String),
    Column('status', Boolean, default=True)
)
