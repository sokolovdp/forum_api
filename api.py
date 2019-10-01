from _datetime import datetime

from sanic import Sanic
from sanic.views import HTTPMethodView
from sanic.response import json, text
from tables import users, topics, posts, comments


def row2dict(row, keys) -> dict:
    return {key: row.get(key) for key in keys}


class AsyncTopicView(HTTPMethodView):

    async def get(self, request, topic_id):
        try:
            if int(topic_id):
                query = topics.select().where(users.c.id == int(topic_id))
                row = await request.app.db.fetch_one(query)
                rows = [row, ]
            else:
                query = topics.select()
                rows = await request.app.db.fetch_all(query)
        except Exception as e:
            return json({'error': str(e)}, status=400)
        else:
            return json({'data': [row2dict(r, topics.columns) for r in rows]})

    async def post(self, request, topic_id):
        try:
            query = topics.insert()
            values = {
                'subject': request.json.get('subject'),
                'description': request.json.get('description'),
                'created': datetime.now(),
                'modified': datetime.now(),
                'user_id': 1,  # get from request.session
            }
            await request.app.db.execute(query, values)
        except Exception as e:
            return json({'error': str(e)}, status=400)
        else:
            return json({})

    async def put(self, request, topic_id):
        try:
            query = topics.update().where(topics.c.id == int(topic_id))
            values = {'modified': datetime.now(), }
            descr = request.json.get('description')
            subj = request.json.get('subject')
            if descr:
                values['description'] = descr
            if subj:
                values['subject'] = subj
            await request.app.db.execute(query, values)
        except Exception as e:
            return json({'error': str(e)}, status=400)
        else:
            return json({})

    async def delete(self, request, topic_id):
        try:
            query = topics.delete().where(topics.c.id == int(topic_id))
            await request.app.db.execute(query)
        except Exception as e:
            return json({'error': str(e)}, status=400)
        else:
            return json({})


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
