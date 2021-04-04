import aiohttp_session
from aiohttp import web
import jsonpickle

from ..model import recipe_table, user_table


async def index(request):
    site_name = request.app['config'].get('site_name')
    return web.Response(text=str(site_name))


async def login(request):
    session = await aiohttp_session.get_session(request)
    if 'username' in session:
        return web.json_response({"message": "you can not login cause you are logged in already"}, status=405)

    form = await request.post()
    nickname = form['login']

    if await user_table.has_user(request.app['db'], nickname):
        session["username"] = nickname
        return web.json_response({"message": "Success"}, status=204)

    else:
        return web.json_response({"message": "User does not exist"}, status=404)


async def logout(request):
    session = await aiohttp_session.get_session(request)

    if 'username' in session:
        session.invalidate()
        return web.json_response({"message": "You logged out"}, status=204)

    else:
        return web.json_response({"message": "user was not logged in to log out"}, status=401)


async def get_user_profile(request):  # TODO: Доделать показ профиля пользователя
    session = await aiohttp_session.get_session(request)

    if 'username' in session:
        profile = await user_table.get_profile(request.app['db'], request.query['nickname'])

        if profile is not None:
            return web.json_response({"message": "success", "data": jsonpickle.encode(profile)}, status=200)
        else:
            return web.json_response({"message": "There is not user with such nickname"}, status=404)
    else:
        return web.json_response({"message": "You need login before this"}, status=401)


async def get_first_ten_users(request):
    session = await aiohttp_session.get_session(request)

    if 'username' in session:
        best_users = await recipe_table.get_best_users(request.app['db'])
        return web.json_response({"message": "success", "data": jsonpickle.encode(best_users)}, status=200)

    else:
        return web.json_response({"message": "You need login before this"}, status=401)


async def registration(request):
    form = await request.post()
    nickname = form['nickname']

    if not await user_table.has_user(request.app['db'], nickname):
        await user_table.create_user(request.app['db'], nickname)
        return web.json_response({"message": "User was created successfully"}, status=201)

    else:
        return web.json_response({"message": "Such user exists"}, status=409)


async def add_recipe(request):
    session = await aiohttp_session.get_session(request)

    if 'username' in session:
        nickname = session.get('username')
        author = await user_table.get_ID_by_nickname(request.app['db'], nickname)

        form = await request.post()
        recipe_name = form['recipe_name']
        info = form['info']
        cooking_steps = form['cooking_steps']
        food_type = form['food_type']
        hashtag_set = form['hashtag_set']

        await recipe_table.create_recipe(request.app['db'], author, recipe_name, info, cooking_steps, food_type, hashtag_set)
        return web.json_response({"message": "recipe was created successfully"}, status=201)

    else:
        return web.json_response({"message": "You need login before this"}, status=401)


async def get_recipes_list(request):  # TODO: Добавить пагинацию и сортирвоку
    session = await aiohttp_session.get_session(request)

    if 'username' in session:
        recipes = await recipe_table.get_recipes(request.app['db'])
        return web.json_response({"message": "Success", "data": jsonpickle.encode(recipes)}, status=200)

    else:
        return web.json_response({"message": "You need login before this"}, status=401)


async def get_recipe(request):  # TODO: Добавить данные пользователя
    session = await aiohttp_session.get_session(request)

    if 'username' in session:
        recipe_id = int(request.query['recipe'])
        recipe = await recipe_table.get_recipe_by_id(request.app['db'], recipe_id)
        if recipe is None:
            return web.json_response({"message": "There is not such recipe"}, status=404)
        else:
            return web.json_response({"message": "success", "data": jsonpickle.encode(recipe)}, status=200)
    else:
        return web.json_response({"message": "You need login before this"}, status=401)


async def block_recipe(request):
    session = await aiohttp_session.get_session(request)

    if 'username' in session:
        if is_admin(request, session.get('username')):
            form = await request.post()
            recipe_id = int(form['recipe'])

            if await recipe_table.has_recipe(request.app['db'], recipe_id):
                await recipe_table.change_recipe_status(request.app['db'], recipe_id, status=False)
                return web.json_response({"message": "success"}, status=204)

            else:
                return web.json_response({"message": "There is not recipe with such id"}, status=404)

        else:
            return web.json_response({"message": "only admin can do this"}, status=403)

    else:
        return web.json_response({"message": "You need login before this"}, status=401)


async def unblock_recipe(request):
    session = await aiohttp_session.get_session(request)

    if 'username' in session:
        if is_admin(request, session.get('username')):
            form = await request.post()
            recipe_id = int(form['recipe'])

            if await recipe_table.has_recipe(request.app['db'], recipe_id):
                await recipe_table.change_recipe_status(request.app['db'], recipe_id, status=True)
                return web.json_response({"message": "success"}, status=204)

            else:
                return web.json_response({"message": "There is not recipe with such id"}, status=404)

        else:
            return web.json_response({"message": "only admin can do this"}, status=403)

    else:
        return web.json_response({"message": "You need login before this"}, status=401)


async def unblock_user(request):
    session = await aiohttp_session.get_session(request)

    if 'username' in session:
        if is_admin(request, session.get('username')):
            form = await request.post()
            user_id = int(form['user_id'])

            if await user_table.has_user_id(request.app['db'], user_id):
                await user_table.change_user_status(request.app['db'], user_id, status=True)
                return web.json_response({"message": "success"}, status=204)

            else:
                return web.json_response({"message": "There is not user with such id"}, status=404)

        else:
            return web.json_response({"message": "only admin can do this"}, status=403)

    else:
        return web.json_response({"message": "You need login before this"}, status=401)


async def block_user(request):
    session = await aiohttp_session.get_session(request)
    if 'username' in session:

        if is_admin(request, session.get('username')):
            form = await request.post()
            user_id = int(form['user_id'])

            if await user_table.has_user_id(request.app['db'], user_id):
                await user_table.change_user_status(request.app['db'], user_id, status=False)
                return web.json_response({"message": "success"}, status=204)

            else:
                return web.json_response({"message": "There is not user with such id"}, status=404)

        else:
            return web.json_response({"message": "only admin can do this"}, status=403)

    else:
        return web.json_response({"message": "You need login before this"}, status=401)


def is_admin(request, username):
    is_admin_flag = False
    for admin_login in request.app['admin']:
        if username == admin_login:
            is_admin_flag = True
    return is_admin_flag
