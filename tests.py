import os

from sanic import Sanic

from tables import setup_database
from middlewares import setup_middlewares
from api import setup_routes


if __name__ == "__main__":
    app = Sanic('forum_api', strict_slashes=os.getenv('USE_STRICT_SLASHES', False))
    setup_database(app)
    setup_routes(app)
    setup_middlewares(app)
    app.run(host="0.0.0.0", port=8000, debug=True, access_log=True, auto_reload=False)
