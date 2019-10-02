from datetime import datetime

from sanic import Sanic
from sanic.views import HTTPMethodView
from sanic.response import json

import tables
from tables import topics, posts, comments  # users,


def get_user_id(request):
    """ Mock function to mimic getting user id from request.session"""
    return 1


def get_pagination_args(request) -> tuple:
    per_page = request.args.get('per_page')
    try:
        per_page = int(per_page)
    except (ValueError, TypeError):
        return None, None
    page = request.args.get('page')
    try:
        page = int(page)
    except (ValueError, TypeError):
        return None, None

    return per_page, per_page * (page - 1)


def row2dict(row: dict, keys: list) -> dict:
    """ Convert row object into dict with str keys, by striping table name"""

    def strip_table_name_from_key(key) -> str:
        return str(key).split('.', 1)[1]

    return {strip_table_name_from_key(key): row.get(key) for key in keys}


class AsyncTopicView(HTTPMethodView):

    async def get(self, request, topic_id):
        try:
            topic_id = int(topic_id)
            if topic_id:
                query = topics.select().where(topics.c.id == topic_id)
                rows = await request.app.db.fetch_all(query)
            else:
                per_page, offset = get_pagination_args(request)
                query = topics.select().order_by('created')
                if per_page:
                    query = query.limit(per_page).offset(offset)
                rows = await request.app.db.fetch_all(query)
        except Exception as e:
            return json({'error': str(e)}, status=400)
        else:
            return json({'topics': [row2dict(r, topics.columns) for r in rows]})

    async def post(self, request, topic_id):
        try:
            query = topics.insert().returning(topics.c.id)
            values = {
                'subject': request.json.get('subject'),
                'description': request.json.get('description'),
                'created': datetime.now(),
                'modified': datetime.now(),
                'user_id': get_user_id(request),
            }
            new_id = await request.app.db.execute(query, values)
        except Exception as e:
            return json({'error': str(e)}, status=400)
        else:
            return json({'id': new_id})

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
            return json({{'id': topic_id}})

    async def delete(self, request, topic_id):
        try:
            query = topics.delete().where(topics.c.id == int(topic_id))
            await request.app.db.execute(query)
        except Exception as e:
            return json({'error': str(e)}, status=400)
        else:
            return json({'id': topic_id})


class AsyncPostView(HTTPMethodView):

    async def get(self, request, topic_id, post_id):
        try:
            topic_id = int(topic_id)
            post_id = int(post_id)
            data = {'post': None, 'comments': []}
            if post_id:
                query = posts.select().where(posts.c.id == post_id)
                row = await request.app.db.fetch_one(query)
                if row:
                    post_data = row2dict(row, posts.columns)
                    data['post'] = post_data
                    query = comments.select().where(comments.c.post_id == post_id)
                    rows = await request.app.db.fetch_all(query)
                    if rows:
                        data['comments'] = [row2dict(r, comments.columns) for r in rows]
            else:
                per_page, offset = get_pagination_args(request)
                query = posts.select().where(posts.c.topic_id == topic_id).order_by('created')
                if per_page:
                    query = query.limit(per_page).offset(offset)
                rows = await request.app.db.fetch_all(query)
                data = {'posts': [row2dict(r, posts.columns) for r in rows]}
        except Exception as e:
            return json({'error': str(e)}, status=400)
        else:
            return json(data)

    async def post(self, request, topic_id, post_id):
        try:
            query = posts.insert().returning(posts.c.id)
            values = {
                'subject': request.json.get('subject'),
                'description': request.json.get('description'),
                'topic_id': int(topic_id),
                'created': datetime.now(),
                'modified': datetime.now(),
                'user_id': get_user_id(request),
            }
            new_id = await request.app.db.execute(query, values)
        except Exception as e:
            return json({'error': str(e)}, status=400)
        else:
            return json({'id': new_id})

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
            return json({'id': post_id})

    async def delete(self, request, topic_id, post_id):
        try:
            query = posts.delete().where(posts.c.id == int(post_id))
            await request.app.db.execute(query)
        except Exception as e:
            return json({'error': str(e)}, status=400)
        else:
            return json({'id': post_id})


async def create_comment(request):
    try:
        query = comments.insert().returning(comments.c.id)
        values = {
            'text': request.json.get('text'),
            'comment_id': request.json.get('comment_id'),
            'topic_id': request.json.get('topic_id'),
            'post_id': request.json.get('post_id'),
            'created': datetime.now(),
            'user_id': get_user_id(request),
        }
        new_id = await request.app.db.execute(query, values)
    except Exception as e:
        return json({'error': str(e)}, status=400)
    else:
        return json({'id': new_id})


async def search_subject(request):
    try:
        args = list(request.args.keys())
        if not args or args[0] not in ('posts', 'topics'):
            raise ValueError('invalid table name, allowed names are: "posts" & "topics"')
        table_name = args[0]
        pattern = request.args.get(table_name)
        if not pattern:
            raise ValueError(f'no search pattern')
        table = getattr(tables, table_name)
        query = table.select().where(table.c.subject.ilike(f'%{pattern}%')).order_by('created')
        rows = await request.app.db.fetch_all(query)
    except Exception as e:
        return json({'error': str(e)}, status=400)
    else:
        return json([row2dict(r, table.columns) for r in rows])


def setup_routes(app: Sanic):
    app.add_route(AsyncTopicView.as_view(), '/topic/<topic_id>')
    app.add_route(AsyncPostView.as_view(), '/topic/<topic_id>/post/<post_id>')
    app.add_route(create_comment, '/comment', methods=['POST'])
    app.add_route(search_subject, '/search', methods=['GET'])
