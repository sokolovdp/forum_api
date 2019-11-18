from sanic import Sanic

from tables import setup_database, setup_mongodb
from middlewares import setup_middleware
from api import setup_routes
from auth import setup_jwt
import forum_config

app = Sanic('forum_api', load_env=forum_config.LOAD_ENV, strict_slashes=forum_config.STRICT_SLASHES)
app.config.from_object(forum_config)

if forum_config.DATABASE_TYPE == 'postgres':
    setup_database(app)
else:
    setup_mongodb(app)

setup_routes(app)
setup_middleware(app)
setup_jwt(app)

if __name__ == "__main__":
    app.run(
        host=app.config.get('HOST', '0.0.0.0'),
        port=app.config.get('PORT', 8000),
        debug=app.config.get('DEBUG', False),
        auto_reload=app.config.get('AUTO_RELOAD', False),
        workers=app.config.get('WORKERS', 1),
    )
