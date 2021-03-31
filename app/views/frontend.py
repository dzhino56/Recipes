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
    if "username" in session:
        return web.Response(text='you can not login cause you are logged in already'), 405

    form = await request.post()
    nickname = form['login']

    async with request.app['db'].acquire() as conn:
        query = select(db.user).where(db.user.c.nickname == nickname)
        result = await conn.fetchrow(query)
        if result is not None:
            session["username"] = nickname
            return {"message": "Success"}, 204
        else:
            return {"message": "User does not exist"}, 404


async def logout(request):
    session = await aiohttp_session.get_session(request)
    if 'username' in session:
        session.invalidate()
        return {"message": "You logged out"}, 204
    else:
        return {"message": "user was not logged in to log out"}, 405


async def get_user_profile(request):  # TODO: Доделать показ профиля пользователя
    session = await aiohttp_session.get_session(request)
    if 'username' in session:
        user_id = request.query['user_id']

        async with request.app['db'].acquire() as conn:
            query = select([db.user.c.user_id, db.user.c.nickname, db.user.c.status]) \
                .where(db.user.c.user_id == user_id)
            result = await conn.fetchrow(query)
            if result is not None:
                return {"message": "success", "data": result}, 200
            else:
                return {"message": "There is not user with such id"}, 404
    else:
        return {"message": "You need login before this"}, 405


async def get_first_ten_users(request):
    session = await aiohttp_session.get_session(request)
    if 'username' in session:
        async with request.app['db'].acquire() as conn:
            query = select([db.recipe.c.author, func.count()]). \
                group_by(db.recipe.c.author). \
                order_by(func.count()).limit(10)
            result = await conn.fetch(query)
            return {"message": "success", "data": result}, 200
    else:
        return {"message": "You need login before this"}, 405


async def registration(request):
    session = await aiohttp_session.get_session(request)
    if 'username' not in session:
        form = await request.post()
        nickname = form['nickname']
        async with request.app['db'].acquire() as conn:
            query = select(db.user).where(db.user.c.nickname == nickname)
            result = await conn.fetchrow(query)
            if result is None:
                query = insert(db.user).values({'nickname': nickname})
                await conn.execute(query)
                return {"message": "User was created successfully"}, 201
            else:
                return {"message": "Such user exists"}, 409
    else:
        return {"message": "You need login before this"}, 405


async def add_recipe(request):
    session = await aiohttp_session.get_session(request)
    if 'username' in session:
        form = await request.post()

        async with request.app['db'].acquire() as conn:
            query = select(db.user).where(db.user.c.nickname == session.get('username'))
            author = await conn.fetchrow(query)

        recipe_name = form['recipe_name']
        info = form['info']
        cooking_steps = form['cooking_steps']
        food_type = form['food_type']
        hashtag_set = form['hashtag_set']

        async with request.app['db'].acquire() as conn:
            query = insert(db.recipe). \
                values(author=author, recipe_name=recipe_name,
                       info=info, cooking_steps=cooking_steps,
                       food_type=food_type, hashtag_set=hashtag_set)
            result = await conn.fetch(query)

            return {"message": "recipe was created successfully"}, 201
    else:
        return {"message": "You need login before this"}, 405


async def get_recipes_list(request):  # TODO: Добавить пагинацию и сортирвоку
    session = await aiohttp_session.get_session(request)
    if 'username' in session:
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
    else:
        return {"message": "You need login before this"}, 405


async def get_recipe(request):  # TODO: Добавить данные пользователя
    session = await aiohttp_session.get_session(request)
    if 'username' in session:
        recipe_id = int(request.query['recipe'])
        async with request.app['db'].acquire() as conn:
            query = select([db.recipe]). \
                where(db.recipe.c.recipe_id == recipe_id)
            result = await conn.fetchrow(query)
            if result is None:
                return {"message": "There is not such recipe"}, 404
            else:
                return {"message": "success", "data": result}, 200
    else:
        return {"message": "You need login before this"}, 405


async def block_recipe(request):
    session = await aiohttp_session.get_session(request)

    if 'username' in session:
        if is_admin(request, session.get('username')):
            async with request.app['db'].acquire() as conn:
                form = await request.post()
                recipe_id = form['recipe']

                query = select(db.recipe) \
                    .where(db.recipe.c.recipe_id == recipe_id)
                result = await conn.fetchrow(query)

                if result is not None:
                    query = update(db.recipe). \
                        values({'status': 'False'}). \
                        where(db.recipe.c.recipe_id == recipe_id)
                    result = await conn.fetch(query)

                    return {"message": "success"}, 204
                else:
                    return {"message": "There is not recipe with such id"}, 404
        else:
            return {"message": "only admin can do this"},
    else:
        return {"message": "You need login before this"}, 405


async def unblock_recipe(request):
    session = await aiohttp_session.get_session(request)

    if 'username' in session:
        if is_admin(request, session.get('username')):

            async with request.app['db'].acquire() as conn:
                form = await request.post()
                recipe_id = form['recipe']

                query = select(db.recipe) \
                    .where(db.recipe.c.recipe_id == recipe_id)
                result = await conn.fetchrow(query)

                if result is not None:
                    query = update(db.recipe). \
                        values({'status': 'True'}). \
                        where(db.recipe.c.recipe_id == recipe_id)
                    result = await conn.fetch(query)

                    return {"message": "success"}, 204
                else:
                    return {"message": "There is not recipe with such id"}, 404
        else:
            return {"message": "only admin can do this"},
    else:
        return {"message": "You need login before this"}, 405


async def unblock_user(request):
    session = await aiohttp_session.get_session(request)

    if 'username' in session:
        if is_admin(request, session.get('username')):

            async with request.app['db'].acquire() as conn:
                form = await request.post()
                user_id = form['user']

                query = select(db.user) \
                    .where(db.user.c.user_id == user_id)
                result = await conn.fetchrow(query)

                if result is not None:
                    query = update(db.user). \
                        values({'status': 'False'}). \
                        where(db.user.c.user_id == user_id)

                    await conn.fetch(query)

                    return {"message": "success"}, 204
                else:
                    return {"message": "There is not user with such id"}, 404
        else:
            return {"message": "only admin can do this"},
    else:
        return {"message": "You need login before this"}, 405


async def block_user(request):
    session = await aiohttp_session.get_session(request)

    if 'username' in session:
        if is_admin(request, session.get('username')):

            async with request.app['db'].acquire() as conn:
                form = await request.post()
                user_id = form['user']

                query = select(db.user) \
                    .where(db.user.c.user_id == user_id)
                result = await conn.fetchrow(query)

                if result is not None:
                    query = update(db.user). \
                        values({'status': 'True'}). \
                        where(db.user.c.user_id == user_id)
                    result = await conn.fetch(query)

                    return {"message": "success"}, 204
                else:
                    return {"message": "There is not user with such id"}, 404
        else:
            return {"message": "only admin can do this"},
    else:
        return {"message": "You need login before this"}, 405


def is_admin(request, username):
    is_admin_flag = False
    for admin_login in request.app['admin']:
        if username == admin_login:
            is_admin_flag = True
    return is_admin_flag
