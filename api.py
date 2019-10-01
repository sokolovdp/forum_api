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
                query = topics.select().where(topics.c.id == int(topic_id))
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

    async def get(self, request, post_id):
        try:
            if int(post_id):
                query = posts.select().where(posts.c.id == int(post_id))
                row = await request.app.db.fetch_one(query)
                rows = [row, ]
            else:
                query = posts.select()
                rows = await request.app.db.fetch_all(query)
        except Exception as e:
            return json({'error': str(e)}, status=400)
        else:
            return json({'data': [row2dict(r, posts.columns) for r in rows]})

    async def post(self, request, post_id):
        try:
            query = posts.insert()
            values = {
                'subject': request.json.get('subject'),
                'description': request.json.get('description'),
                'topic_id': request.json.get('topic_id'),
                'created': datetime.now(),
                'modified': datetime.now(),
                'user_id': 1,  # get from request.session
            }
            await request.app.db.execute(query, values)
        except Exception as e:
            return json({'error': str(e)}, status=400)
        else:
            return json({})

    async def put(self, request, post_id):
        try:
            query = posts.update().where(posts.c.id == int(post_id))
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

    async def delete(self, request, post_id):
        try:
            query = posts.delete().where(posts.c.id == int(post_id))
            await request.app.db.execute(query)
        except Exception as e:
            return json({'error': str(e)}, status=400)
        else:
            return json({})


async def create_comment(request):
    return text('Create comment')


async def list_comments(request, topic_id, post_id):
    return text('list comments')


def setup_routes(app: Sanic):
    app.add_route(AsyncTopicView.as_view(), '/topic/<topic_id>')
    app.add_route(AsyncPostView.as_view(), '/topic/<topic_id>/post/<post_id>')
    app.add_route(create_comment, '/comment/<comment_id>', methods=['POST', ])
    app.add_route(list_comments, '/topic/<topic_id>/post/<post_id>/comments', methods=['GET', ])
