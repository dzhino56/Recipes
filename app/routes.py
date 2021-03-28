from .views import frontend
from aiohttp import web


def setup_routes(app):
    app.router.add_routes([web.get('/', frontend.index),
                           web.get('/users/user', frontend.get_user_profile),
                           web.get('/users/top_users', frontend.get_first_ten_users),
                           # web.get('/users/block_user', frontend.block_user),
                           # web.get('/users/unblock_user', frontend.unblock_user),

                           web.post('/users/new_user', frontend.registration),

                           web.get('/recipes/recipe', frontend.get_recipe),
                           web.get('/recipes/block_recipe', frontend.block_recipe),
                           # web.get('/recipes/unblock_recipe', frontend.unblock_recipe),

                           web.post('/recipes/new_recipe', frontend.add_recipe),

                           web.get('/recipes', frontend.get_recipes_list),
                           ])
