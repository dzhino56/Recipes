from aiohttp import web
from .routes import setup_routes


async def create_app(config: dict):
    app = web.Application()
    app['config'] = config
    setup_routes(app)
    return app
