import os

from sqlalchemy import create_engine
from sqlalchemy.exc import DBAPIError
from psycopg2.errorcodes import DUPLICATE_TABLE

import tables
import auth


if __name__ == '__main__':
    database_url = os.getenv('SANIC_DATABASE_URL')

    print(f'creating forum api tables, database url="{database_url}" ...')

    db_engine = create_engine(database_url, echo=True)
    db_connection = db_engine.connect()
    try:
        tables.users.create(db_connection)
        tables.topics.create(db_connection)
        tables.posts.create(db_connection)
        tables.comments.create(db_connection)
    except DBAPIError as db_error:
        if db_error.orig.pgcode == DUPLICATE_TABLE:
            print('\nforum tables already exists!\n')
            exit(0)
        else:
            raise db_error

    query = tables.users.insert()
    db_connection.execute(query, auth.INITIAL_ADMIN_DATA)

    print('\nforum api tables, and admin user created\n')
