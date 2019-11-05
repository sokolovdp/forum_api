import os

# Sanic app parameters
STRICT_SLASHES = False
LOAD_ENV = True

# Sanic run parameters
HOST = "0.0.0.0"
DEBUG = True
AUTO_RELOAD = False
WORKERS = 1

# Sanic JWT parameters
AUTH_MODE = True
SECRET = os.getenv('SANIC_JWT_SECRET', 'very_secret_string')
ACCESS_TOKEN_NAME = 'JWT'

# Admin User data
ADMIN_LOGIN = os.getenv('ADMIN_NAME', 'admin')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin')
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')

API_ERROR = 400
