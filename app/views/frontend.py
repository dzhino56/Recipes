import aiohttp_session
from aiohttp import web

from ..model import recipe_table, user_table


async def index(request):
    site_name = request.app['config'].get('site_name')
    return web.Response(text=str(site_name))


async def login(request):
    session = await aiohttp_session.new_session(request)
    if 'username' in session:
        return web.Response(text='you can not login cause you are logged in already'), 405

    form = await request.post()
    nickname = form['login']

    if user_table.has_user(request, nickname):
        session["username"] = nickname
        return {"message": "Success"}, 204

    else:
        return {"message": "User does not exist"}, 404


async def logout(request):
    session = await aiohttp_session.new_session(request)
    if 'username' in session:
        session.invalidate()
        return {"message": "You logged out"}, 204
    else:
        return {"message": "user was not logged in to log out"}, 405


async def get_user_profile(request):  # TODO: Доделать показ профиля пользователя
    session = await aiohttp_session.new_session(request)

    if 'username' in session:
        profile = user_table.get_profile(request, request.query['nickname'])

        if profile is not None:
            return {"message": "success", "data": profile}, 200
        else:
            return {"message": "There is not user with such id"}, 404
    else:
        return {"message": "You need login before this"}, 405


async def get_first_ten_users(request):
    session = await aiohttp_session.new_session(request)

    if 'username' in session:
        best_users = recipe_table.get_best_users(request)
        return {"message": "success", "data": best_users}, 200

    else:
        return {"message": "You need login before this"}, 405


async def registration(request):
    session = await aiohttp_session.new_session(request)

    if 'username' not in session:
        form = await request.post()
        nickname = form['nickname']

        user = user_table.get_by_nickname(request, nickname)
        if user is None:
            user_table.create_user(request, nickname)
            return {"message": "User was created successfully"}, 201

        else:
            return {"message": "Such user exists"}, 409

    else:
        return {"message": "You need login before this"}, 405


async def add_recipe(request):
    session = await aiohttp_session.new_session(request)

    if 'username' in session:
        nickname = session.get('username')
        author = user_table.get_by_nickname(request, nickname)

        form = await request.post()
        recipe_name = form['recipe_name']
        info = form['info']
        cooking_steps = form['cooking_steps']
        food_type = form['food_type']
        hashtag_set = form['hashtag_set']

        recipe_table.create_recipe(request, author, recipe_name, info, cooking_steps, food_type, hashtag_set)
        return {"message": "recipe was created successfully"}, 201

    else:
        return {"message": "You need login before this"}, 405


async def get_recipes_list(request):  # TODO: Добавить пагинацию и сортирвоку
    session = await aiohttp_session.new_session(request)

    if 'username' in session:
        recipes = recipe_table.get_recipes(request)
        return {"message": "Success", "data": recipes}, 200

    else:
        return {"message": "You need login before this"}, 405


async def get_recipe(request):  # TODO: Добавить данные пользователя
    session = await aiohttp_session.new_session(request)

    if 'username' in session:
        recipe_id = int(request.query['recipe'])
        recipe = recipe_table.get_recipe_by_id(request, recipe_id)
        if recipe is None:
            return {"message": "There is not such recipe"}, 404
        else:
            return {"message": "success", "data": recipe}, 200
    else:
        return {"message": "You need login before this"}, 405


async def block_recipe(request):
    session = await aiohttp_session.new_session(request)

    if 'username' in session:
        if is_admin(request, session.get('username')):
            form = await request.post()
            recipe_id = int(form['recipe'])

            recipe = recipe_table.get_recipe_by_id(request, recipe_id)

            if recipe is not None:
                recipe_table.change_recipe_status(request, recipe_id, status=False)
                return {"message": "success"}, 204

            else:
                return {"message": "There is not recipe with such id"}, 404

        else:
            return {"message": "only admin can do this"},

    else:
        return {"message": "You need login before this"}, 405


async def unblock_recipe(request):
    session = await aiohttp_session.new_session(request)

    if 'username' in session:
        if is_admin(request, session.get('username')):
            form = await request.post()
            recipe_id = form['recipe']

            recipe = recipe_table.get_recipe_by_id(request, recipe_id)

            if recipe is not None:
                recipe_table.change_recipe_status(request, recipe_id, status=True)
                return {"message": "success"}, 204

            else:
                return {"message": "There is not recipe with such id"}, 404

        else:
            return {"message": "only admin can do this"},

    else:
        return {"message": "You need login before this"}, 405


async def unblock_user(request):
    session = await aiohttp_session.new_session(request)

    if 'username' in session:
        if is_admin(request, session.get('username')):
            form = await request.post()
            nickname = form['nickname']

            user = user_table.get_by_nickname(request, nickname)

            if user is not None:
                user_table.change_user_status(request, nickname, status=True)
                return {"message": "success"}, 204

            else:
                return {"message": "There is not user with such id"}, 404

        else:
            return {"message": "only admin can do this"},

    else:
        return {"message": "You need login before this"}, 405


async def block_user(request):
    session = await aiohttp_session.new_session(request)
    if 'username' in session:

        if is_admin(request, session.get('username')):
            form = await request.post()
            nickname = form['nickname']

            if user_table.has_user(request, nickname):
                user_table.change_user_status(request, nickname, status=False)
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
