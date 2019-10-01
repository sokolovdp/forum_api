from typing import Any
import os

from sanic import Sanic
from databases import Database

from middlewares import setup_middlewares
from api import setup_routes


def get_env_bool(name: str, default=False) -> bool:
    true_str = {'1', 'yes', 'true'}
    var = os.environ.get(name, None)
    if var is None:
        return default
    return var.lower() in true_str


def create_sanic_app(name: str, **kwargs: Any) -> Sanic:
    kwargs['strict_slashes'] = os.getenv('USE_STRICT_SLASHES', False)
    return Sanic(name, **kwargs)


def setup_database(app: Sanic):
    db_url = os.environ.get('DATABASE_URL')
    app.db = Database(db_url)

    @app.listener('after_server_start')
    async def connect_to_db(*args):
        await app.db.connect()

    @app.listener('after_server_stop')
    async def disconnect_from_db(*args):
        await app.db.disconnect()


if __name__ == "__main__":
    sanic_app = create_sanic_app('forum_api')
    setup_database(sanic_app)
    setup_routes(sanic_app)
    setup_middlewares(sanic_app)
    sanic_app.run(host="0.0.0.0", port=8000, debug=True, access_log=True, auto_reload=False)
