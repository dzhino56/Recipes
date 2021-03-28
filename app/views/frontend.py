from aiohttp import web
from sqlalchemy import func
from sqlalchemy.sql.expression import select
from sqlalchemy.sql.expression import insert
from sqlalchemy.sql.expression import update

from ..model import recipe
from ..model import user


async def index(request):
    site_name = request.app['config'].get('site_name')
    return web.Response(text=str(site_name))


async def get_user_profile(request):  # TODO: Доделать показ профиля пользователя
    async with request.app['db'].acquire() as conn:
        query = select([user.user.c.user_id, user.user.c.nickname, user.user.c.status])
        return web.Response(text=str(query))


async def get_first_ten_users(request):
    async with request.app['db'].acquire() as conn:
        query = select([recipe.recipe.c.author, func.count()]). \
            group_by(recipe.recipe.c.author). \
            order_by(func.count()).limit(10)
        return web.Response(text=str(query))


async def registration(request):  # TODO: Проверка на то, что пользователь с таким ником существует
    nickname = request.query['nickname']
    async with request.app['db'].acquire() as conn:
        query = insert(user.user).values(nickname=nickname)
        return web.Response(text=str(query))


async def enter(request):
    pass


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
        query = insert(recipe.recipe). \
            values(author=author, recipe_name=recipe_name,
                   info=info, cooking_steps=cooking_steps,
                   food_type=food_type, hashtag_set=hashtag_set)
        return web.Response(text=str(query))


async def get_recipes_list(request):  # TODO: Добавить пагинацию и сортирвоку
    async with request.app['db'].acquire() as conn:
        query = select([recipe.recipe.c.recipe_id,
                        recipe.recipe.c.author,
                        recipe.recipe.c.datetime,
                        recipe.recipe.c.recipe_name,
                        recipe.recipe.c.info,
                        recipe.recipe.c.photo,
                        recipe.recipe.c.food_type,
                        recipe.recipe.c.likes_count,
                        recipe.recipe.c.hashtag_set,
                        ]). \
            where(recipe.recipe.c.status == True)
        return web.Response(text=str(query))


async def get_recipe(request):  # TODO: Добавить данные пользователя
    recipe_id = request.query['recipe']
    async with request.app['db'].acquire() as conn:
        query = select([recipe.recipe]).where(recipe.recipe.c.recipe_id == recipe_id)
        return web.Response(text=str(query))


# async def block_recipe(request):
#     async with request.app['db'].acquire() as conn:
#         recipe_id = request.query['recipe']
#         query = update(recipe.recipe).values(recipe.recipe.c.status=False).where(recipe.recipe.c.recipe_id == recipe_id)
#         return web.Response(text=str(query))
#
#
# async def unblock_recipe(request):
#     async with request.app['db'].acquire() as conn:
#         recipe_id = request.query['recipe']
#         query = update(recipe.recipe).values(recipe.recipe.c.status = True).where(recipe.recipe.c.recipe_id == recipe_id)
#         return web.Response(text=str(query))
#
#
# async def unblock_user(request):
#     async with request.app['db'].acquire() as conn:
#         recipe_id = request.query['recipe']
#         query = update(user.user).values(user.user.c.status = True).where(
#             user.user.c.user_id == user_id)
#         return web.Response(text=str(query))
#
# async def block_user(request):
#     async with request.app['db'].acquire() as conn:
#         user_id = request.query['recipe']
#         query = update(user.user).values(user.user.c.status = False).where(
#             user.user.c.user_id == user_id)
#         return web.Response(text=str(query))
