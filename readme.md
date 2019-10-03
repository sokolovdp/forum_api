#

To start API tests on another port change port values in docker-compose file in two lines:
`
      - SANIC_PORT=8000
      ...
      - "8000:8000"
`

## Link to Postman collection with forum api tests
https://www.getpostman.com/collections/317be8f6281d97c259f2