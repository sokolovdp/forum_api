# Forum API - demo implementation of the Async Rest API.

## Used packages:
- Python 3.7.4
- Sanic - async framework
- databases - package which uses *asyncpg* to implement an asynchronous library for PostgreSQL
- SQLAlchemy Core - expression language
- secure - package which implements some security improvements, by ensuring use of X-XSS-Protection, Strict-Transport-Security and other headers 

## To run demo forum api application
- download repo folder *forum_api* from GitHub to your computer
- from folder run: 
`
docker-compose up
`
- during startup process application will init DB tables and run tests
- forum api by default listens port *8000*, so you  can access api at: localhost:8000
- API's urls are:
`
/topic/<topic_id>
/topic/<topic_id>/post/<post_id>
/comment
/search
`
- no authorization is required, by default during db initialization created two users with IDs: 1 and 2
- to get list of topics or all posts in the given topic use *0* as topic_id or post_id

## Paginating mode
To get list of all topics or all posts in the given topic in paginating mode, provide *page* and *per_page*  in the query string

## To run application on the different port
To use different port, change values in docker-compose file in two lines:
`
      - SANIC_PORT=8000
      ...
      - "8000:8000"
`
## To test Link to Postman collection with forum api tests
https://www.getpostman.com/collections/317be8f6281d97c259f2
