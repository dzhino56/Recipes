from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import Text
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime

from datetime import datetime
from .. import app
__all__ = ('user', 'recipe')

meta = MetaData()

user = Table(
    "user", meta,

    Column('user_id', Integer, primary_key=True),
    Column('nickname', String, unique=True),
    Column('status', Boolean, default=True),
    Column('favourite', Text, default='')
)


recipe = Table(
    "recipe", meta,

    Column('recipe_id', Integer, primary_key=True),
    Column('author', Integer, ForeignKey('user.user_id')),
    Column('datetime', DateTime, default=datetime.now()),
    Column('recipe_name', String),
    Column('info', String),
    Column('cooking_steps', String),
    # Column('photo', ),  # ???????????????????????????
    Column('food_type', String),
    Column('likes_count', Integer, default=0),
    Column('hashtag_set', String),
    Column('status', Boolean, default=True)
)
