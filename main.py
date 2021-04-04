from aiohttp import web
from app import create_app
from settings import load_config


app = create_app(config=load_config())

if __name__ == '__main__':
    web.run_app(app, port=8765)
