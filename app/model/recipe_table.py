from datetime import datetime

from sqlalchemy import Table, MetaData, Column, Integer, ForeignKey, DateTime, String, Boolean
from sqlalchemy.sql.expression import select
from sqlalchemy.sql.expression import insert
from sqlalchemy.sql.expression import update
from sqlalchemy import func


meta = MetaData()

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


async def get_best_users(pool):
    async with pool.acquire() as conn:
        query = select([recipe.c.author, func.count()]). \
            group_by(recipe.c.author). \
            order_by(func.count()).limit(10)
        return await conn.fetch(query)


async def create_recipe(pool, author, recipe_name, info, cooking_steps, food_type, hashtag_set):
    async with pool.acquire() as conn:
        query = insert(recipe). \
            values(author=author, recipe_name=recipe_name,
                   info=info, cooking_steps=cooking_steps,
                   food_type=food_type, hashtag_set=hashtag_set)
        await conn.fetch(query)


async def get_recipes(pool):
    async with pool.acquire() as conn:
        query = select([recipe.c.recipe_id,
                        recipe.c.author,
                        recipe.c.datetime,
                        recipe.c.recipe_name,
                        recipe.c.info,
                        # recipe.c.photo,
                        recipe.c.food_type,
                        recipe.c.likes_count,
                        recipe.c.hashtag_set,
                        ]). \
            where(recipe.c.status == True)

        return await conn.fetch(query)


async def get_recipe_by_id(pool, recipe_id):
    async with pool.acquire() as conn:
        query = select([recipe]). \
            where(recipe.c.recipe_id == recipe_id)
        return await conn.fetchrow(query)


async def change_recipe_status(pool, recipe_id, status):
    async with pool.acquire() as conn:
        query = update(recipe). \
            values({'status': status}). \
            where(recipe.c.recipe_id == recipe_id)
        await conn.fetch(query)


async def has_recipe(pool, recipe_id):
    return await get_recipe_by_id(pool, recipe_id) is not None
