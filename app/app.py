from aiohttp import web
from .routes import setup_routes
import asyncpgsa


async def create_app(config: dict):
    app = web.Application()
    app['config'] = config
    setup_routes(app)
    app.on_startup.append(on_start)
    app.on_cleanup.append(on_finish)
    return app


async def on_start(app):
    config = app['config']
    app['db'] = await asyncpgsa.create_pool(dsn=config['DATABASE_URI'])


async def on_finish(app):
    await app['db'].close()
