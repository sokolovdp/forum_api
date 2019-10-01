from datetime import datetime

from sanic import Sanic
from sanic.views import HTTPMethodView
from sanic.response import json  # , text
from sqlalchemy.sql import select, and_  # , or_, not_

from tables import users, topics, posts, comments


def row2dict(row, keys) -> dict:
    return {key: row.get(key) for key in keys}


class AsyncTopicView(HTTPMethodView):

    async def get(self, request, topic_id):
        """
        Retrieve all or one topic
        :param request: sanic request object
        :param topic_id: 0 - return all topics, otherwise - topic with given ID
        :return:  list of dicts or dict with error
        """
        try:
            topic_id = int(topic_id)
            if topic_id:
                query = topics.select().where(topics.c.id == topic_id)
                rows = await request.app.db.fetch_all(query)
                data = [row2dict(r, topics.columns) for r in rows]
            else:
                query = topics.select().order_by('created')
                rows = await request.app.db.fetch_all(query)
                data = [row2dict(r, topics.columns) for r in rows]
        except Exception as e:
            return json({'error': str(e)}, status=400)
        else:
            return json({'data': data})

    async def post(self, request, topic_id):
        """
        Create topic
        :param request: sanic request object
        :param topic_id:  ignored
        :return: empty dict or dict with error
        """
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

    async def get(self, request, topic_id, post_id):
        try:
            topic_id = int(topic_id)
            post_id = int(post_id)
            if post_id:
                query = select([posts, comments]).where(posts.c.id == post_id)
                rows = await request.app.db.fetch_all(query)
                data = [row2dict(r, posts.columns + comments.columns) for r in rows]
            else:
                query = posts.select().where(posts.c.topic_id == topic_id).order_by('created')
                rows = await request.app.db.fetch_all(query)
                data = [row2dict(r, posts.columns) for r in rows]
        except Exception as e:
            return json({'error': str(e)}, status=400)
        else:
            return json({'data': data})

    async def post(self, request, topic_id, post_id):
        try:
            query = posts.insert()
            values = {
                'subject': request.json.get('subject'),
                'description': request.json.get('description'),
                'topic_id': int(topic_id),
                'created': datetime.now(),
                'modified': datetime.now(),
                'user_id': 1,  # get from request.session
            }
            await request.app.db.execute(query, values)
        except Exception as e:
            return json({'error': str(e)}, status=400)
        else:
            return json({})

    async def put(self, request, topic_id, post_id):
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

    async def delete(self, request, topic_is, post_id):
        try:
            query = posts.delete().where(posts.c.id == int(post_id))
            await request.app.db.execute(query)
        except Exception as e:
            return json({'error': str(e)}, status=400)
        else:
            return json({})


class AsyncCommentView(HTTPMethodView):

    async def get(self, request, topic_id, post_id):
        try:
            query = comments.select().where(
                and_(
                    comments.c.topic_id == int(topic_id),
                    comments.c.post_id == int(post_id),
                )
            ).order_by('created')
            rows = await request.app.db.fetch_all(query)
        except Exception as e:
            return json({'error': str(e)}, status=400)
        else:
            return json({'data': [row2dict(r, comments.columns) for r in rows]})

    async def post(self, request, topic_id, post_id):
        try:
            query = comments.insert()
            values = {
                'text': request.json.get('text'),
                'comment_id': request.json.get('comment_id'),
                'topic_id': int(topic_id),
                'post_id': int(post_id),
                'created': datetime.now(),
                'user_id': 1,  # get from request.session
            }
            await request.app.db.execute(query, values)
        except Exception as e:
            return json({'error': str(e)}, status=400)
        else:
            return json({})


def setup_routes(app: Sanic):
    app.add_route(AsyncTopicView.as_view(), '/topic/<topic_id>')
    app.add_route(AsyncPostView.as_view(), '/topic/<topic_id>/post/<post_id>')
    app.add_route(AsyncCommentView.as_view(), 'topic/<topic_id>/post/<post_id>/comments')
