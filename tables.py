import os

from sanic import Sanic
from sqlalchemy import MetaData, Table, Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from databases import Database

metadata = MetaData()

users = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True),
    Column('login', String(50), unique=True, nullable=False),
    Column('password', String(50), nullable=False),
    Column('email', String(50), unique=True, nullable=False),
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

tables_map = {
    'posts': posts,
    'topics': topics,
    'comments': comments,
    'users': users
}


def setup_database(app: Sanic):
    db_url = os.environ.get('DATABASE_URL')
    app.db = Database(db_url)

    @app.listener('after_server_start')
    async def connect_to_db(*args):
        await app.db.connect()

    @app.listener('after_server_stop')
    async def disconnect_from_db(*args):
        await app.db.disconnect()