from datetime import datetime

from sanic import Sanic
from sanic.views import HTTPMethodView
from sanic.response import json

from python_paginate.web.sanic_paginate import Pagination

from tables import users, topics, posts, comments, tables_map


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

    return per_page,  per_page * (page - 1)


def row2dict(row: dict, keys: list) -> dict:
    """ Convert row object into dict with str keys"""
    return {str(key): row.get(key) for key in keys}


def cut_keys(dict_list: dict) -> dict:
    """ Remove from key 'table.field' name of the table"""
    return {key.split('.')[1]: value for key, value in dict_list.items()}


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
                per_page, offset = get_pagination_args(request)
                query = topics.select().order_by('created')
                if per_page:
                    query = query.limit(per_page).offset(offset)
                rows = await request.app.db.fetch_all(query)
                data = [row2dict(r, topics.columns) for r in rows]
        except Exception as e:
            return json({'error': str(e)}, status=400)
        else:
            return json({'topics': [cut_keys(d) for d in data]})

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
            data = {'post': None, 'comments': []}
            if post_id:
                query = posts.select().where(posts.c.id == post_id)
                row = await request.app.db.fetch_one(query)
                if row:
                    post_data = cut_keys(row2dict(row, posts.columns))
                    data['post'] = post_data
                    query = comments.select().where(comments.c.post_id == post_id)
                    rows = await request.app.db.fetch_all(query)
                    if rows:
                        data['comments'] = [cut_keys(row2dict(r, comments.columns)) for r in rows]
            else:
                per_page, offset = get_pagination_args(request)
                query = posts.select().where(posts.c.topic_id == topic_id).order_by('created')
                if per_page:
                    query = query.limit(per_page).offset(offset)
                rows = await request.app.db.fetch_all(query)
                data = {'posts': [cut_keys(row2dict(r, posts.columns)) for r in rows]}
        except Exception as e:
            return json({'error': str(e)}, status=400)
        else:
            return json(data)

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


async def create_comment(request):
    try:
        query = comments.insert()
        values = {
            'text': request.json.get('text'),
            'comment_id': request.json.get('comment_id'),
            'topic_id': request.json.get('topic_id'),
            'post_id': request.json.get('post_id'),
            'created': datetime.now(),
            'user_id': 1,  # get from request.session
        }
        await request.app.db.execute(query, values)
    except Exception as e:
        return json({'error': str(e)}, status=400)
    else:
        return json({})


async def search_subject(request):
    try:
        args = list(request.args.keys())
        if not args or args[0] not in ('posts', 'topics'):
            raise ValueError('invalid table name, allowed names are: "posts" & "topics"')
        table_name = args[0]
        pattern = request.args.get(table_name)
        if not pattern:
            raise ValueError(f'no search pattern')
        table = tables_map[table_name]
        query = table.select().where(table.c.subject.ilike(f'%{pattern}%')).order_by('created')
        rows = await request.app.db.fetch_all(query)
        data = [cut_keys(row2dict(r, table.columns)) for r in rows]
    except Exception as e:
        return json({'error': str(e)}, status=400)
    else:
        return json(data)


def setup_routes(app: Sanic):
    app.add_route(AsyncTopicView.as_view(), '/topic/<topic_id>')
    app.add_route(AsyncPostView.as_view(), '/topic/<topic_id>/post/<post_id>')
    app.add_route(create_comment, '/comment', methods=['POST'])
    app.add_route(search_subject, '/search', methods=['GET'])
