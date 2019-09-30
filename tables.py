from sqlalchemy import MetaData, Table, Column, Integer, String, Text, DateTime, ForeignKey

metadata = MetaData()

topics = Table(
    'topics', metadata,
    Column('id', Integer, primary_key=True),
    Column('subject', String(length=256), unique=True, nullable=False),
    Column('description', Text()),
    Column('created', DateTime()),
    Column('modified', DateTime()),
)

posts = Table(
    'posts', metadata,
    Column('id', Integer, primary_key=True),
    Column('subject', String(length=256), unique=True, nullable=False),
    Column('description', Text(), nullable=False),
    Column('created', DateTime(), nullable=False),
    Column('modified', DateTime(), nullable=False),
    Column('topic_id', Integer, ForeignKey('topics.id', ondelete="DELETE"), nullable=False),
)

comments = Table(
    'comment', metadata,
    Column('id', Integer, primary_key=True),
    Column('text', Text(), nullable=False),
    Column('created', DateTime()),
    Column('post_id', Integer, ForeignKey('posts.id', ondelete="DELETE"), nullable=False),
    Column('comment_id', Integer, ForeignKey('comment.id', ondelete="DELETE"), nullable=True),
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
