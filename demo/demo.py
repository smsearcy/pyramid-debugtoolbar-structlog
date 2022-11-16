"""Basic Pyramid application to demonstrate the structlog panel."""

from wsgiref.simple_server import make_server

import structlog
from pyramid.config import Configurator
from pyramid.request import Request

logger = structlog.get_logger()


def home(request: Request):
    logger.msg("Home visited", ip=request.remote_addr, path=request.path_qs)
    return {}


def make_app():
    settings = {}
    settings["pyramid.reload_templates"] = True
    settings["debugtoolbar.hosts"] = ["127.0.0.1"]
    settings["debugtoolbar.intercept_redirects"] = True
    settings["debugtoolbar.includes"] = "pyramid_debugtoolbar_structlog"
    config = Configurator(settings=settings)
    config.add_route("home", "/")
    config.add_view(home, route_name="home", renderer="home.mako")
    config.include("pyramid_mako")
    config.include("pyramid_debugtoolbar")
    return config.make_wsgi_app()


if __name__ == "__main__":
    app = make_app()
    server = make_server("127.0.0.1", 6543, app)
    print("Serving app at http://127.0.0.1:6543")
    server.serve_forever()
