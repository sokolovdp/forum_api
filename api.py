from sanic import Sanic

# from api_postgres import AsyncPostView, AsyncTopicView, create_comment, search_subject
from api_mongodb import AsyncPostView, AsyncTopicView, create_comment, search_subject


def setup_routes(app: Sanic):
    app.add_route(AsyncTopicView.as_view(), '/topic/<topic_id>')
    app.add_route(AsyncPostView.as_view(), '/topic/<topic_id>/post/<post_id>')
    app.add_route(create_comment, '/comment', methods=['POST'])
    app.add_route(search_subject, '/search', methods=['GET'])
