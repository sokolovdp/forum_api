# Forum API - demo implementation of the async Rest API.

## Used packages:
- Python 3.7.4
- Sanic - async framework
- databases - package which uses *asyncpg* to implement fast asynchronous library for PostgreSQL  (see https://github.com/MagicStack/asyncpg )
- SQLAlchemyCore - expression language
- secure - package which implements some security improvements, by ensuring use of X-XSS-Protection, Strict-Transport-Security and other headers 
- Docker and docker-compose

## To run demo Forum API application
- you need docker and docker-compose to be installed
- download or clone repo *forum_api* from GitHub to your computer
- in the forum_api folder run command: 
`
docker-compose up
`

- forum API by default listens port *8000*, so you can access API at: *localhost:8000*
- API's urls are:

`
/topic/<topic_id> ... 
/topic/<topic_id>/post/<post_id> ... 
/comment ... 
/search
`
- no user authorization is required, by default during DB initialization created two users with IDs: 1 and 2
- to get list of topics or all posts in the given topic use *0* as topic_id or post_id

`
GET localhost:8000/topic/0 ... 
GET localhost:8000/topic/1/post/0
`

## Paginating mode
To get list of all topics or all posts in the given topic in paginating mode, provide *page* and *per_page* values in the query string

`
GET localhost:8000/topic/0?page=1&per_page=10 ... 
GET localhost:8000/topic/1/post/0?page=2&per_page=30
`

## To run API application on the different port
To use different port, change port value in the *docker-compose* file in these two lines:

`
    - SANIC_PORT=8000
    ...
    - "8000:8000"
`
## Auto testing API
During container start docker will run 3 python scripts:
- init_db.py - to connect DB and initialize required tables
- tests.py - to run auto tests 
- forum.py - to start and run API 

## To test API in the Postman
Import collection *forum-api* into Postman from this link:

https://www.getpostman.com/collections/317be8f6281d97c259f2

You can run them all at once in Collection runner, or play one by one with different data

