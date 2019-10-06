from sanic import Sanic

from tables import setup_database
from middlewares import setup_middleware
from api import setup_routes
from auth import setup_jwt

app = Sanic('forum_api', load_env=True, strict_slashes=False)
setup_database(app)
setup_routes(app)
setup_middleware(app)
setup_jwt(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=app.config['PORT'], debug=True, auto_reload=False)
