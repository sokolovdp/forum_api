import os
import pymongo

import tables
import auth

if __name__ == '__main__':
    mongodb_url = os.getenv('SANIC_DATABASE_URL')
    mongo_client = pymongo.MongoClient(mongodb_url)

    print(f'creating forum api collections, mongodb url="{mongodb_url}" ...')

    mdb = mongo_client['forum_db']  # create forum database
    for col in (tables.Users, tables.Topics, tables.Posts, tables.Comments):  # create collections
        _ = mdb[col.__coll__]

    mdb.users.create_index([('login', pymongo.ASCENDING), ], unique=True)

    try:
        mdb.users.insert_one(auth.INITIAL_ADMIN_DATA)
    except pymongo.errors.DuplicateKeyError:
        print('\nadmin user already exists!\n')

    print('\nforum api collections, and admin user created\n')
