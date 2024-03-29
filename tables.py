from sanic import Sanic
from sqlalchemy import MetaData, Table, Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from databases import Database
from sanic_motor import BaseModel, AsyncIOMotorClient

metadata = MetaData()

users = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True),
    Column('login', String(80), unique=True, nullable=False),
    Column('password', String(256), nullable=False),
    Column('email', String(80), unique=True, nullable=False),
    Column('admin', Boolean, nullable=False),
)

topics = Table(
    'topics', metadata,
    Column('id', Integer, primary_key=True),
    Column('subject', String(length=256), unique=True, nullable=False),
    Column('description', Text()),
    Column('created', DateTime()),
    Column('modified', DateTime()),
    Column('user_id', Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False),
)

posts = Table(
    'posts', metadata,
    Column('id', Integer, primary_key=True),
    Column('subject', String(length=256), unique=True, nullable=False),
    Column('description', Text(), nullable=False),
    Column('created', DateTime(), nullable=False),
    Column('modified', DateTime(), nullable=False),
    Column('topic_id', Integer, ForeignKey('topics.id', ondelete="CASCADE"), nullable=False),
    Column('user_id', Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False),
)

comments = Table(
    'comments', metadata,
    Column('id', Integer, primary_key=True),
    Column('text', Text(), nullable=False),
    Column('created', DateTime()),
    Column('user_id', Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False),
    Column('topic_id', Integer, ForeignKey('topics.id', ondelete="CASCADE"), nullable=False),
    Column('post_id', Integer, ForeignKey('posts.id', ondelete="CASCADE"), nullable=False),
    Column('comment_id', Integer, ForeignKey('comments.id', ondelete="CASCADE"), nullable=True),
)


def row2dict(row: dict, keys: list) -> dict:
    """ Convert row object into dict with str keys, by striping table name"""

    def strip_table_name_from_key(key) -> str:
        return str(key).split('.', 1)[1]

    return {strip_table_name_from_key(key): row.get(key) for key in keys}


def setup_database(app: Sanic):
    app.db = Database(app.config['DATABASE_URL'])

    @app.listener('after_server_start')
    async def connect_to_db(*args):
        await app.db.connect()

    @app.listener('after_server_stop')
    async def disconnect_from_db(*args):
        await app.db.disconnect()


class Users(BaseModel):
    __coll__ = 'users'
    __unique_fields__ = ['login', 'password', 'email', 'admin']


class Topics(BaseModel):
    __coll__ = 'topics'
    __unique_fields__ = ['subject', 'description', 'created', 'modified', 'user_id']


class Posts(BaseModel):
    __coll__ = 'posts'
    __unique_fields__ = ['subject', 'description', 'created', 'modified', 'topic_id', 'user_id']


class Comments(BaseModel):
    __coll__ = 'comments'
    __unique_fields__ = ['text', 'created', 'modified', 'user_id', 'topic_id', 'post_id', 'comment_id']


def doc2dict(collection, doc):
    result_dict = {key: str(getattr(doc, key)) for key in collection.__unique_fields__}
    result_dict['id'] = str(doc._id)
    return result_dict


MONGO_DB_NAME = 'forum_db'


def setup_mongodb(app: Sanic):
    motor_settings = {
        'MOTOR_URI': app.config['DATABASE_URL'] + '/' + MONGO_DB_NAME,
        'LOGO': None,
    }
    app.config.update(motor_settings)
    BaseModel.init_app(app)

    @app.listener('before_server_start')
    async def connect_to_db(*args):
        app.db = AsyncIOMotorClient(app.config['DATABASE_URL'])[MONGO_DB_NAME]

    @app.listener('after_server_stop')
    async def disconnect_from_db(*args):
        pass

