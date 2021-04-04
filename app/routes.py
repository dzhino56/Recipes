from .views import frontend
from aiohttp import web


def setup_routes(app):
    app.router.add_routes([web.get('/', frontend.index),

                           web.patch('/users/block_user', frontend.block_user),
                           web.patch('/users/unblock_user', frontend.unblock_user),
                           web.get('/users/user', frontend.get_user_profile),
                           web.get('/users', frontend.get_first_ten_users),

                           web.post('/users', frontend.registration),

                           web.post('/login', frontend.login),
                           web.post('/logout', frontend.logout),

                           web.get('/recipes/recipe', frontend.get_recipe),
                           web.patch('/recipes/block_recipe', frontend.block_recipe),
                           web.patch('/recipes/unblock_recipe', frontend.unblock_recipe),
                           web.post('/recipes', frontend.add_recipe),
                           web.get('/recipes', frontend.get_recipes_list),
                           ])
