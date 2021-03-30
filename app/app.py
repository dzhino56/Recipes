import asyncpgsa
import aiohttp_session
from aiohttp import web
from sqlalchemy.schema import DropTable
from sqlalchemy.schema import CreateTable

from .routes import setup_routes
from .model import db


async def create_app(config: dict):
    app = web.Application()
    app['config'] = config
    setup_routes(app)
    aiohttp_session.setup(app, aiohttp_session.SimpleCookieStorage())
    app.on_startup.append(on_start)
    app.on_cleanup.append(on_finish)
    return app


async def delete_tables(app, tables):
    async with app['db'].acquire() as conn:
        for table in reversed(tables):
            drop_expr = DropTable(table)
            await conn.execute(drop_expr)


async def prepare_tables(app):
    tables = [db.user, db.recipe]
    # await delete_tables(app, tables)
    async with app['db'].acquire() as conn:
        for table in tables:
            create_expr = CreateTable(table)
            await conn.execute(create_expr)


async def on_start(app):
    config = app['config']
    app['db'] = await asyncpgsa.create_pool(dsn=config['DATABASE_URI'])
    # await prepare_tables(app)


async def on_finish(app):
    await app['db'].close()
