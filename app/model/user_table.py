from sqlalchemy import MetaData, Table, Column, Integer, String, Boolean, Text
from sqlalchemy.sql.expression import select
from sqlalchemy.sql.expression import insert
from sqlalchemy.sql.expression import update


meta = MetaData()

user = Table(
    "user", meta,

    Column('user_id', Integer, primary_key=True),
    Column('nickname', String, unique=True),
    Column('status', Boolean, default=True),
    Column('favourite', Text, default='')
)


def get_by_nickname(request, nickname):
    async with request.app['db'].acquire() as conn:
        query = select(user).where(user.c.nickname == nickname)
        return await conn.fetchrow(query)


def get_profile(request, user_id):
    async with request.app['db'].acquire() as conn:
        query = select([user.c.user_id, user.c.nickname, user.c.status]) \
            .where(user.c.user_id == user_id)
        return await conn.fetchrow(query)


def create_user(request, nickname):
    async with request.app['db'].acquire() as conn:
        query = insert(user).values({'nickname': nickname})
        await conn.execute(query)


def change_user_status(request, nickname, status):
    async with request.app['db'].acquire() as conn:
        query = update(user). \
            values({'status': status}). \
            where(user.c.nickname == nickname)

        await conn.fetch(query)


def has_user(request, nickname):
    return get_by_nickname(request, nickname) is not None
