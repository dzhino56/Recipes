from aiohttp import web


def index(request):
    site_name = request.app['config'].get('site_name')
    return web.Response(text=site_name)
