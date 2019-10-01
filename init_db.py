import os
from sqlalchemy import create_engine
import tables

if __name__ == '__main__':
    db_engine = create_engine(os.getenv('DATABASE_URL'), echo=True)
    db_connection = db_engine.connect()

    tables.users.create(db_connection)
    tables.topics.create(db_connection)
    tables.posts.create(db_connection)
    tables.comments.create(db_connection)

    query = tables.users.insert()
    values = [
        {
            'login': 'admin',
            'password': 'admin',
            'email': 'admin@mail.ru',
            'admin': True
        },
        {
            'login': 'user',
            'password': 'user',
            'email': 'user@mail.ru',
            'admin': False
        },
    ]
    db_connection.execute_many(query, values)