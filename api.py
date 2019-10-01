from _datetime import datetime

from sanic import Sanic
from sanic.views import HTTPMethodView
from sanic.response import json, text
# from sqlalchemy_paginator import Paginator
from tables import users, topics, posts, comments


class AsyncTopicView(HTTPMethodView):

    async def get(self, request, topic_id):
        if int(topic_id):
            result = 'retrive one'
        else:
            result = 'retrive all'
        return text(result)

    async def post(self, request, topic_id):

        return json(request.json)

    async def put(self, request, topic_id):

        return json(request.json)

    async def delete(self, request, topic_id):
        if not int(topic_id):
            return json({'error': 'invalid id'}, status=400)
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
    app.add_route(AsyncTopicView.as_view(), '/topic/<topic_id>')
    app.add_route(AsyncPostView.as_view(), '/post/<post_id>')
    app.add_route(create_comment, '/comment', methods=['POST', 'GET'])
