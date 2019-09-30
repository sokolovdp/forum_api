import sqlalchemy as sa

metadata = sa.MetaData()

topics = sa.Table(
    'topic',
    metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('subject', sa.String(length=256), unique=True, nullable=False),
    sa.Column('description', sa.Text()),
    sa.Column('created', sa.DateTime()),
    sa.Column('modified', sa.DateTime()),
)

posts = sa.Table(
    'post',
    metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('subject', sa.String(length=256), unique=True, nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('modified', sa.DateTime(), nullable=False),
    sa.Column('topic_id', sa.Integer, sa.ForeignKey('topic.id', ondelete="DELETE"), nullable=False),
)

comments = sa.Table(
    'comment',
    metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('text', sa.Text(), nullable=False),
    sa.Column('created', sa.DateTime()),
    sa.Column('post_id', sa.Integer, sa.ForeignKey('post.id', ondelete="DELETE"), nullable=False),
    sa.Column('comment_id', sa.Integer, sa.ForeignKey('comment.id', ondelete="DELETE"), nullable=True),
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
