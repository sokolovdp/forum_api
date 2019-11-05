from datetime import datetime

from sanic.views import HTTPMethodView
from sanic.response import json
from sanic.log import logger
from sanic_jwt.decorators import protected


import tables
from tables import Topics, Posts, Comments  # Users,

API_ERROR = 400


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


class AsyncTopicView(HTTPMethodView):
    # decorators = [protected()]

    async def get(self, request, topic_id):
        try:
            if topic_id:
                topic = await Topics.find_one(topic_id)
                topics = [topic, ]
            else:
                per_page, offset = get_pagination_args(request)
                topics = await Topics.find(sort='created')
                if per_page:  # todo handle paginating
                    pass
        except Exception as e:
            logger.error('get topic(s) error=%s', str(e))
            return json({'error': str(e)}, status=API_ERROR)
        else:
            return json({'topics': topics})

    async def post(self, request, topic_id):
        try:
            values = {
                'subject': request.json.get('subject'),
                'description': request.json.get('description'),
                'created': datetime.now(),
                'modified': datetime.now(),
                'user_id': get_user_id(request),
            }
            new_id = await Topics.insert_one(values)
        except Exception as e:
            logger.error('create topic error=%s', str(e))
            return json({'error': str(e)}, status=API_ERROR)
        else:
            logger.info('created new topic id=%s', new_id)
            return json({'id': new_id})

    async def put(self, request, topic_id):
        try:
            topic = await Topics.find_one(topic_id)
            if not topic:
                return json({'error': f'invalid topic_id: {topic_id}'}, status=API_ERROR)
            values = {'modified': datetime.now(), }
            descr = request.json.get('description')
            subj = request.json.get('subject')
            if descr:
                values['description'] = descr
            if subj:
                values['subject'] = subj
            topic.clean_for_dirty(values)
            await Topics.update_one({'_id': topic.id}, {'$set': values})
        except Exception as e:
            logger.error('update topic error=%s', str(e))
            return json({'error': str(e)}, status=API_ERROR)
        else:
            logger.info('updated topic id=%s', topic_id)
            return json({'id': topic_id})

    async def delete(self, request, topic_id):
        try:
            topic = await Topics.find_one(topic_id)
            if not topic:
                return json({'error': f'invalid topic_id: {topic_id}'}, status=API_ERROR)
            await topic.destroy()
        except Exception as e:
            logger.error('delete topic error=%s', str(e))
            return json({'error': str(e)}, status=API_ERROR)
        else:
            return json({'id': topic_id})


class AsyncPostView(HTTPMethodView):
    # decorators = [protected()]

    # async def get(self, request, topic_id, post_id):
    #     try:
    #         topic_id = int(topic_id)
    #         post_id = int(post_id)
    #         data = {'post': None, 'comments': []}
    #         if post_id:
    #             query = sql.select(posts.columns + comments.columns).select_from(
    #                 posts.outerjoin(comments, comments.c.post_id == post_id)
    #             ).where(posts.c.id == post_id)
    #             rows = await request.app.db.fetch_all(query)
    #             if rows:
    #                 data['post'] = row2dict(rows[0], posts.columns)
    #                 result = [row2dict(r, comments.columns) for r in rows]
    #                 if result[0]['id'] is not None:
    #                     data['comments'] = result
    #         else:
    #             per_page, offset = get_pagination_args(request)
    #             query = posts.select().where(posts.c.topic_id == topic_id).order_by('created')
    #             if per_page:
    #                 query = query.limit(per_page).offset(offset)
    #             rows = await request.app.db.fetch_all(query)
    #             data = {'posts': [row2dict(r, posts.columns) for r in rows]}
    #     except Exception as e:
    #         logger.error('list post(s) error=%s', str(e))
    #         return json({'error': str(e)}, status=API_ERROR)
    #     else:
    #         return json(data)
    #
    # async def post(self, request, topic_id, post_id):
    #     try:
    #         query = posts.insert().returning(posts.c.id)
    #         values = {
    #             'subject': request.json.get('subject'),
    #             'description': request.json.get('description'),
    #             'topic_id': int(topic_id),
    #             'created': datetime.now(),
    #             'modified': datetime.now(),
    #             'user_id': get_user_id(request),
    #         }
    #         new_id = await request.app.db.execute(query, values)
    #     except Exception as e:
    #         logger.error('create post error=%s', str(e))
    #         return json({'error': str(e)}, status=API_ERROR)
    #     else:
    #         logger.info('created post id=%s', new_id)
    #         return json({'id': new_id})
    #
    # async def put(self, request, topic_id, post_id):
    #     try:
    #         query = posts.update().where(posts.c.id == int(post_id))
    #         values = {'modified': datetime.now(), }
    #         descr = request.json.get('description')
    #         subj = request.json.get('subject')
    #         if descr:
    #             values['description'] = descr
    #         if subj:
    #             values['subject'] = subj
    #         await request.app.db.execute(query, values)
    #     except Exception as e:
    #         logger.error('update post error=%s', str(e))
    #         return json({'error': str(e)}, status=API_ERROR)
    #     else:
    #         logger.info('updated post id=%s', post_id)
    #         return json({'id': post_id})
    #
    # async def delete(self, request, topic_id, post_id):
    #     try:
    #         query = posts.delete().where(posts.c.id == int(post_id))
    #         await request.app.db.execute(query)
    #     except Exception as e:
    #         logger.error('delete post error=%s', str(e))
    #         return json({'error': str(e)}, status=API_ERROR)
    #     else:
    #         logger.info('deleted post id=%s', post_id)
    #         return json({'id': post_id})
    pass

# @protected()
async def create_comment(request):
    # try:
    #     query = comments.insert().returning(comments.c.id)
    #     values = {
    #         'text': request.json.get('text'),
    #         'comment_id': request.json.get('comment_id'),
    #         'topic_id': request.json.get('topic_id'),
    #         'post_id': request.json.get('post_id'),
    #         'created': datetime.now(),
    #         'user_id': get_user_id(request),
    #     }
    #     new_id = await request.app.db.execute(query, values)
    # except Exception as e:
    #     logger.error('create comment error=%s', str(e))
    #     return json({'error': str(e)}, status=API_ERROR)
    # else:
    #     logger.info('created comment id=%s', new_id)
    #     return json({'id': new_id})
    pass


# @protected()
async def search_subject(request):
    # try:
    #     args = list(request.args.keys())
    #     if not args or args[0] not in ('posts', 'topics'):
    #         raise ValueError('invalid table name, allowed names are: "posts" & "topics"')
    #     table_name = args[0]
    #     pattern = request.args.get(table_name)
    #     if not pattern:
    #         raise ValueError(f'no search pattern')
    #     table = getattr(tables, table_name)
    #     query = table.select().where(table.c.subject.ilike(f'%{pattern}%')).order_by('created')
    #     rows = await request.app.db.fetch_all(query)
    # except Exception as e:
    #     logger.error('search error=%s', str(e))
    #     return json({'error': str(e)}, status=API_ERROR)
    # else:
    #     return json([row2dict(r, table.columns) for r in rows])
    pass
