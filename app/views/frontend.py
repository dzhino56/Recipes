import aiohttp_session
from aiohttp import web
from sqlalchemy import func
from sqlalchemy.sql.expression import select
from sqlalchemy.sql.expression import insert
from sqlalchemy.sql.expression import update

from ..model import db


async def index(request):
    site_name = request.app['config'].get('site_name')
    return web.Response(text=str(site_name))


async def login(request):
    session = await aiohttp_session.new_session(request)
    form = await request.post()
    session["username"] = form['login']
    return web.Response(text=session["username"])


async def logout(request: web.Request):
    session = await aiohttp_session.get_session(request)
    session.invalidate()
    return web.Response(text='you logged out')


async def get_user_profile(request):  # TODO: Доделать показ профиля пользователя
    user_id = request.query['user_id']

    async with request.app['db'].acquire() as conn:
        query = select([db.user.c.user_id, db.user.c.nickname, db.user.c.status]) \
            .where(db.user.c.user_id == user_id)
        result = await conn.fetchrow(query)
        if result is not None:
            return {"message": "success", "data": result}, 200
        return {"message": "There is not user with such id"}, 404


async def get_first_ten_users(request):
    async with request.app['db'].acquire() as conn:
        query = select([db.recipe.c.author, func.count()]). \
            group_by(db.recipe.c.author). \
            order_by(func.count()).limit(10)
        result = await conn.fetch(query)
        return {"message": "success", "data": result}, 200


async def registration(request):
    nickname = request.query['nickname']
    async with request.app['db'].acquire() as conn:
        query = select(db.user).where(db.user.c.nickname == nickname)
        result = await conn.fetchrow(query)
        if result is None:
            query = insert(db.user).values({'nickname': nickname})
            await conn.execute(query)
            return {"message": "User was created successfully"}, 201
        return {"message": "Such user exists"}, 409


async def go_away(request):
    pass


async def add_recipe(request):
    author = request.query['author']
    recipe_name = request.query['recipe_name']
    info = request.query['info']
    cooking_steps = request.query['cooking_steps']
    food_type = request.query['food_type']
    hashtag_set = request.query['hashtag_set']

    async with request.app['db'].acquire() as conn:
        query = insert(db.recipe). \
            values(author=author, recipe_name=recipe_name,
                   info=info, cooking_steps=cooking_steps,
                   food_type=food_type, hashtag_set=hashtag_set)
        result = await conn.fetch(query)

        return {"message": "recipe was created successfully"}, 201


async def get_recipes_list(request):  # TODO: Добавить пагинацию и сортирвоку
    async with request.app['db'].acquire() as conn:
        query = select([db.recipe.c.recipe_id,
                        db.recipe.c.author,
                        db.recipe.c.datetime,
                        db.recipe.c.recipe_name,
                        db.recipe.c.info,
                        # db.recipe.c.photo,
                        db.recipe.c.food_type,
                        db.recipe.c.likes_count,
                        db.recipe.c.hashtag_set,
                        ]). \
            where(db.recipe.c.status == True)

        result = await conn.fetch(query)
        return {"message": "Success", "data": result}, 200


async def get_recipe(request):  # TODO: Добавить данные пользователя
    recipe_id = int(request.query['recipe'])
    async with request.app['db'].acquire() as conn:
        query = select([db.recipe]). \
            where(db.recipe.c.recipe_id == recipe_id)
        result = await conn.fetchrow(query)
        if result is None:
            return {"message": "There is not such recipe"}, 404
        return {"message": "success", "data": result}, 200


async def block_recipe(request):
    async with request.app['db'].acquire() as conn:
        recipe_id = request.query['recipe']
        query = select(db.recipe) \
            .where(db.recipe.c.recipe_id == recipe_id)
        result = await conn.fetchrow(query)
        if result is not None:
            query = update(db.recipe). \
                values({'status': 'False'}). \
                where(db.recipe.c.recipe_id == recipe_id)
            result = await conn.fetch(query)
            return {"message": "success"}, 204
        return {"message": "There is not recipe with such id"}, 404


async def unblock_recipe(request):
    async with request.app['db'].acquire() as conn:
        recipe_id = request.query['recipe']
        query = select(db.recipe) \
            .where(db.recipe.c.recipe_id == recipe_id)
        result = await conn.fetchrow(query)
        if result is not None:
            query = update(db.recipe). \
                values({'status': 'True'}). \
                where(db.recipe.c.recipe_id == recipe_id)
            result = await conn.fetch(query)
            return {"message": "success"}, 204
        return {"message": "There is not recipe with such id"}, 404


async def unblock_user(request):
    async with request.app['db'].acquire() as conn:
        user_id = request.query['user']
        query = select(db.user) \
            .where(db.user.c.user_id == user_id)
        result = await conn.fetchrow(query)
        if result is not None:
            query = update(db.user). \
                values({'status': 'False'}). \
                where(db.user.c.user_id == user_id)
            await conn.fetch(query)
            return {"message": "success"}, 204
        return {"message": "There is not user with such id"}, 404


async def block_user(request):
    async with request.app['db'].acquire() as conn:
        user_id = request.query['user']
        query = select(db.user) \
            .where(db.user.c.user_id == user_id)
        result = await conn.fetchrow(query)
        if result is not None:
            query = update(db.user). \
                values({'status': 'True'}). \
                where(db.user.c.user_id == user_id)
            result = await conn.fetch(query)
            return {"message": "success"}, 204
        return {"message": "There is not user with such id"}, 404
