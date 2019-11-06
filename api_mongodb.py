from datetime import datetime

from sanic.views import HTTPMethodView
from sanic.response import json
from sanic.log import logger
from sanic_jwt.decorators import protected


import tables
from tables import Topics, Posts, Comments, Users, doc2dict

from forum_config import API_ERROR


async def get_user_id(request):
    """ Mock function to mimic getting user id from request.session"""
    users = await Users.find()
    user = users.objects[0]
    return str(user._id)


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
            if topic_id != '0':
                topic = await Topics.find_one(topic_id)
                topics = [topic, ]
            else:
                per_page, offset = get_pagination_args(request)
                query = await Topics.find(sort='created')
                topics = query.objects
                if per_page:  # todo handle paginating
                    pass
        except Exception as e:
            logger.error('get topic(s) error=%s', str(e))
            return json({'error': str(e)}, status=API_ERROR)
        else:
            topics_list = [doc2dict(Topics, topic) for topic in topics]
            return json({'topics': topics_list})

    async def post(self, request, topic_id):
        try:
            user_id = await get_user_id(request)
            values = {
                'subject': request.json.get('subject'),
                'description': request.json.get('description'),
                'created': datetime.now(),
                'modified': datetime.now(),
                'user_id': user_id,
            }
            new_topic = await Topics.insert_one(values)
        except Exception as e:
            logger.error('create topic error=%s', str(e))
            return json({'error': str(e)}, status=API_ERROR)
        else:
            logger.info('created new topic id=%s', new_topic.inserted_id)
            return json({'id': str(new_topic.inserted_id)})

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
            if topic:
                await topic.destroy()
        except Exception as e:
            logger.error('delete topic error=%s', str(e))
            return json({'error': str(e)}, status=API_ERROR)
        else:
            return json({'id': topic_id})


class AsyncPostView(HTTPMethodView):
    # decorators = [protected()]

    async def get(self, request, topic_id, post_id):
        try:
            if post_id != '0':
                data = {'post': None, 'comments': []}
                post = await Posts.find_one(post_id)
                if post:
                    data['post'] = doc2dict(Posts, post)
                    query2 = await Comments.find(
                        filter={'topic_id': topic_id, 'post_id': post_id},
                        sort='created'
                    )
                    data['comments'] = [doc2dict(Comments, com) for com in query2.objects]
            else:
                per_page, offset = get_pagination_args(request)
                query = await Posts.find(filter={'topic_id': topic_id}, sort='created')
                if per_page:
                    pass
                data = {'posts': [doc2dict(Posts, post) for post in query.objects]}
        except Exception as e:
            logger.error('list post(s) error=%s', str(e))
            return json({'error': str(e)}, status=API_ERROR)
        else:
            return json(data)

    async def post(self, request, topic_id, post_id):
        try:
            user_id = await get_user_id(request)
            values = {
                'subject': request.json.get('subject'),
                'description': request.json.get('description'),
                'topic_id': topic_id,
                'created': datetime.now(),
                'modified': datetime.now(),
                'user_id': user_id,
            }
            new_post = await Posts.insert_one(values)
        except Exception as e:
            logger.error('create post error=%s', str(e))
            return json({'error': str(e)}, status=API_ERROR)
        else:
            logger.info('created post id=%s', str(new_post.inserted_id))
            return json({'id': str(new_post.inserted_id)})

    async def put(self, request, topic_id, post_id):
        try:
            post = await Posts.find_one(post_id)
            if not post:
                return json({'error': f'invalid post_id: {post_id}'}, status=API_ERROR)
            values = {'modified': datetime.now(), }
            descr = request.json.get('description')
            subj = request.json.get('subject')
            if descr:
                values['description'] = descr
            if subj:
                values['subject'] = subj
            post.clean_for_dirty(values)
            await Posts.update_one({'_id': post.id}, {'$set': values})
        except Exception as e:
            logger.error('update post error=%s', str(e))
            return json({'error': str(e)}, status=API_ERROR)
        else:
            logger.info('updated post id=%s', post_id)
            return json({'id': post_id})

    async def delete(self, request, topic_id, post_id):
        try:
            post = await Posts.find_one(post_id)
            if post:
                await post.destroy()
        except Exception as e:
            logger.error('delete post error=%s', str(e))
            return json({'error': str(e)}, status=API_ERROR)
        else:
            logger.info('deleted post id=%s', post_id)
            return json({'id': post_id})


# @protected()
async def create_comment(request):
    try:
        user_id = await get_user_id(request)
        values = {
            'text': request.json.get('text'),
            'comment_id': request.json.get('comment_id'),
            'topic_id': request.json.get('topic_id'),
            'post_id': request.json.get('post_id'),
            'created': datetime.now(),
            'user_id': user_id,
        }
        new_comment = await Comments.insert_one(values)
    except Exception as e:
        logger.error('create comment error=%s', str(e))
        return json({'error': str(e)}, status=API_ERROR)
    else:
        logger.info('created comment id=%s', str(new_comment.inserted_id))
        return json({'id': str(new_comment.inserted_id)})


# @protected()
async def search_subject(request):
    try:
        args = list(request.args.keys())
        if not args or args[0] not in ('posts', 'topics'):
            raise ValueError('invalid table name, allowed names are: "posts" & "topics"')
        table_name = args[0]
        pattern = request.args.get(table_name)
        if not pattern:
            raise ValueError(f'no search pattern')
        collection = getattr(tables, table_name.capitalize())
        query = await collection.find(filter={'subject': f'/{pattern}/'}, sort='created')  # todo proper search !!!
        data = [doc2dict(collection, obj) for obj in query.objects]
    except Exception as e:
        logger.error('search error=%s', str(e))
        return json({'error': str(e)}, status=API_ERROR)
    else:
        return json(data)

