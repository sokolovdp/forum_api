from typing import Any
import os

from sanic import Sanic
from sanic.response import json
from sanic.log import logger
from databases import Database


def create_sanic_app(name: str, **kwargs: Any) -> Sanic:
    """
    Create a Sanic app instance, forcing some default parameters
    and configuring logging, if the config file for that is provided
    in the ``LOGGING_CONFIG_PATH`` environment variable.

    :param name:
    :param kwargs:
    :return: Sanic app instance
    """
    kwargs['load_env'] = True
    # kwargs['configure_logging'] =
    kwargs['strict_slashes'] = os.getenv('USE_STRICT_SLASHES', False)
    return Sanic(name, **kwargs)


def setup_database(sanic_app):
    sanic_app.db = Database(app.config.DB_URL)
    sanic_app.add_listener('after_server_start')

    async def connect_to_db(*args, **kwargs):
        await app.db.connect() @ app.listener('after_server_stop')

    async def disconnect_from_db(*args, **kwargs):
        await app.db.disconnect()


async def test(request):
    return json({"hello": "world"})


if __name__ == "__main__":
    app = create_sanic_app('forum_api')
    app.add_route(test, '/test/', methods=['GET'])
    app.run(host="0.0.0.0", port=8000, debug=True, access_log=True, auto_reload=False)
