from sanic import Sanic
from sanic.views import HTTPMethodView
from sanic.response import json, text
from tables import users, topics, posts, comments


class AsyncTopicView(HTTPMethodView):

    async def get(self, request):
        return text('I am get method')

    async def post(self, request):
        return text('I am post method')

    async def put(self, request):
        return text('I am put method')

    async def delete(self, request):
        return text('I am delete method')


class AsyncPostView(HTTPMethodView):

    async def get(self, request):
        return text('I am get method')

    async def post(self, request):
        return text('I am post method')

    async def put(self, request):
        return text('I am put method')

    async def delete(self, request):
        return text('I am delete method')


async def create_comment(request):
    return text('Create comment')


def setup_routes(app: Sanic):
    app.add_route(AsyncTopicView.as_view(), '/topic')
    app.add_route(AsyncPostView.as_view(), '/post')
    app.add_route(create_comment, '/comment', methods=['POST', 'GET'])
