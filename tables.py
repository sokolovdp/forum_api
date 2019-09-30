import sqlalchemy
from forum import sanic_app

metadata = sqlalchemy.MetaData()

books = sqlalchemy.Table(
    'books',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('title', sqlalchemy.String(length=100)),
    sqlalchemy.Column('author', sqlalchemy.String(length=60)),
)

# Executing many
query = books.insert()
values = [
    {"title": "No Highway", "author": "Nevil Shute"},
    {"title": "The Daffodil", "author": "SkyH. E. Bates"},
]
await sanic_app.db.execute_many(query, values)

# Fetching multiple rows
query = books.select()
rows = await sanic_app.db.fetch_all(query)

# Fetch single row
query = books.select()
row = await sanic_app.db.fetch_one(query)
