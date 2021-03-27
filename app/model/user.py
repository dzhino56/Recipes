from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import Text
from sqlalchemy import MetaData
from sqlalchemy import Table


__all__ = ('user', 'recipe')

meta = MetaData()

user = Table(
    "user", meta,

    Column('user_id', Integer, primary_key=True),
    Column('nickname', String, unique=True),
    Column('status', Boolean),
    Column('favourite', Text)
)
