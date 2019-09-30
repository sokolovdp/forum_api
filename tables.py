from sqlalchemy import MetaData, Table, Column, Integer, String, Text, DateTime, ForeignKey, Boolean

metadata = MetaData()

users = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True),
    Column('login', String(50), nullable=False),
    Column('password', String(50), nullable=False),
    Column('email', String(50), nullable=False),
    Column('admin', Boolean, nullable=False),
)

topics = Table(
    'topics', metadata,
    Column('id', Integer, primary_key=True),
    Column('subject', String(length=256), unique=True, nullable=False),
    Column('description', Text()),
    Column('created', DateTime()),
    Column('modified', DateTime()),
    Column('user_id', Integer, ForeignKey('users.id', ondelete="DELETE"), nullable=False),
)

posts = Table(
    'posts', metadata,
    Column('id', Integer, primary_key=True),
    Column('subject', String(length=256), unique=True, nullable=False),
    Column('description', Text(), nullable=False),
    Column('created', DateTime(), nullable=False),
    Column('modified', DateTime(), nullable=False),
    Column('topic_id', Integer, ForeignKey('topics.id', ondelete="DELETE"), nullable=False),
    Column('user_id', Integer, ForeignKey('users.id', ondelete="DELETE"), nullable=False),
)

comments = Table(
    'comment', metadata,
    Column('id', Integer, primary_key=True),
    Column('text', Text(), nullable=False),
    Column('created', DateTime()),
    Column('post_id', Integer, ForeignKey('posts.id', ondelete="DELETE"), nullable=False),
    Column('comment_id', Integer, ForeignKey('comments.id', ondelete="DELETE"), nullable=True),
    Column('user_id', Integer, ForeignKey('users.id', ondelete="DELETE"), nullable=False),
)

# Executing many
# query = books.insert()
# values = [
#     {"title": "No Highway", "author": "Nevil Shute"},
#     {"title": "The Daffodil", "author": "SkyH. E. Bates"},
# ]
# sanic_app.db.execute_many(query, values)


# Fetching multiple rows
# query = books.select()
# rows = await sanic_app.db.fetch_all(query)

# Fetch single row
# query = books.select()
# row = await sanic_app.db.fetch_one(query)
