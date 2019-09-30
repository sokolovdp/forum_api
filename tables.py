import sqlalchemy as sa

metadata = sa.MetaData()

sections = sa.Table(
    'section',
    metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('subject', sa.String(length=512)),
    sa.Column('description', sa.Text()),
    sa.Column('created', sa.DateTime()),
    sa.Column('modified', sa.DateTime()),
)

posts = sa.Table(
    'post',
    metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('subject', sa.String(length=512)),
    sa.Column('description', sa.Text()),
    sa.Column('created', sa.DateTime()),
    sa.Column('modified', sa.DateTime()),
)

comments = sa.Table(
    'comment',
    metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('description', sa.Text()),
    sa.Column('created', sa.DateTime()),
    sa.Column('modified', sa.DateTime()),
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
