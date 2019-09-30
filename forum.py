from typing import Any
import os

from sanic import Sanic
from sanic.log import logger
from sanic.response import json

from databases import Database

from middlewares import setup_middlewares

import tables


def get_env_bool(name: str, default=False) -> bool:
    TRUE_STR = {'1', 'yes', 'true'}
    var = os.environ.get(name, None)
    if var is None:
        return default
    return var.lower() in TRUE_STR


def create_sanic_app(name: str, **kwargs: Any) -> Sanic:
    # kwargs['load_env'] = True
    # kwargs['configure_logging'] =
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


sanic_app = create_sanic_app('forum_api')


async def test(request):
    # query = tables.books.insert()
    # values = [
    #     {"title": "No Highway", "author": "Nevil Shute"},
    #     {"title": "The Daffodil", "author": "SkyH. E. Bates"},
    # ]
    # await sanic_app.db.execute_many(query, values)

    query = tables.books.select()
    rows = await sanic_app.db.fetch_all(query)
    return json({'books': [{row['title']: row['author']} for row in rows]})

if __name__ == "__main__":
    setup_database(sanic_app)
    sanic_app.add_route(test, '/test', methods=['GET'])
    setup_middlewares(sanic_app)
    sanic_app.run(host="0.0.0.0", port=8000, debug=True, access_log=True, auto_reload=False)
