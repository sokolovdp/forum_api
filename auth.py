import hashlib

from sanic import Sanic
from sanic.request import Request
from sanic_jwt import Initialize, Configuration, exceptions

from sanic.log import logger

from tables import users, row2dict


def hash_password(password):
    salted = password + JwtConfiguration.secret
    return hashlib.sha512(salted.encode("utf8")).hexdigest()


async def authenticate(request: Request, *args, **kwargs):
    login = request.json.get('login', None)
    password = request.json.get('password', None)
    if not login or not password:
        raise exceptions.AuthenticationFailed("missing login or password")

    query = users.select().where(users.c.login == login)
    row = await request.app.db.fetch_one(query)
    if row is None:
        raise exceptions.AuthenticationFailed(f"user with login {login} not found")

    user = row2dict(row, users.columns)
    if hash_password(password) != user['password']:
        logger.info('authentication attempt with invalid password for login %s', login)
        raise exceptions.AuthenticationFailed("user password is incorrect.")

    logger.info('successful authentication for login %s', login)
    return user


class JwtConfiguration(Configuration):
    auth_mode = True
    debug = True
    strict_slashes = False
    access_token_name = 'jwt'
    secret = 'jwt hash string should be provided from the env'
    user_id = 'id'


async def retrieve_user(request, payload, *args, **kwargs):
    if payload:
        user_id = payload.get('user_id', None)
        if user_id is not None:
            query = users.select().where(users.c.id == user_id)
            user = await request.app.db.fetch_one(query)
            return user
    return None


def setup_jwt(app: Sanic):
    Initialize(
        app,
        configuration_class=JwtConfiguration,
        authenticate=authenticate,
        retrieve_user=retrieve_user
    )
