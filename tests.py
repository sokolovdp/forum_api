import json
import unittest
import random
from sanic.log import logger

from forum import app

N = random.randint(1, 10000)

CREATED_TOPIC_ID = None
CREATED_POST_ID = None
CREATED_COMMENT_ID = None


class AutoRestTests(unittest.TestCase):
    """ Unit test cases for Forum Rest APIs  """

    def setUp(self):
        pass

    def test_01_create_topic(self):
        global CREATED_TOPIC_ID

        data = {
            "subject": f"topic {N} subject",
            "description": f"topic {N} description"
        }
        request, response = app.test_client.post('/topic/0', data=json.dumps(data))
        self.assertEqual(response.status, 200)
        data = json.loads(response.text)
        CREATED_TOPIC_ID = int(data['id'])
        logger.info(f'created topic id = {CREATED_TOPIC_ID}')

    def test_02_create_post(self):
        global CREATED_POST_ID

        data = {
            "subject": f"post {N} subject",
            "description": f"post {N} description"
        }
        request, response = app.test_client.post(f'topic/{CREATED_TOPIC_ID}/post/0', data=json.dumps(data))
        self.assertEqual(response.status, 200)
        data = json.loads(response.text)
        CREATED_POST_ID = int(data['id'])
        logger.info(f'created post id = {CREATED_POST_ID}')

    def test_03_create_comment(self):
        global CREATED_COMMENT_ID

        data = {
            "text": f"post {CREATED_POST_ID} comment {N}",
            "comment_id": None,
            "topic_id": CREATED_TOPIC_ID,
            "post_id": CREATED_POST_ID
        }
        request, response = app.test_client.post('/comment', data=json.dumps(data))
        self.assertEqual(response.status, 200)
        data = json.loads(response.text)
        CREATED_COMMENT_ID = int(data['id'])
        logger.info(f'created comment id = {CREATED_COMMENT_ID}')

    def test_04_create_comment_for_comment(self):
        data = {
            "text": f"comment for comment {CREATED_COMMENT_ID}",
            "comment_id": CREATED_COMMENT_ID,
            "topic_id": CREATED_TOPIC_ID,
            "post_id": CREATED_POST_ID
        }
        request, response = app.test_client.post('/comment', data=json.dumps(data))
        self.assertEqual(response.status, 200)
        data = json.loads(response.text)
        logger.info(f'created comment for comment id = {int(data["id"])}')

    def test_05_get_list_of_topics(self):
        request, response = app.test_client.get('/topic/0')
        self.assertEqual(response.status, 200)
        data = json.loads(response.text)
        topic_list = data.get('topics')
        self.assertTrue(topic_list is not None)
        self.assertTrue(len(topic_list) > 0)

    def test_06_get_list_of_posts(self):
        request, response = app.test_client.get(f'/topic/{CREATED_TOPIC_ID}/post/0')
        self.assertEqual(response.status, 200)
        data = json.loads(response.text)
        post_list = data.get('posts')
        self.assertTrue(post_list is not None)
        self.assertTrue(len(post_list) > 0)

    def test_07_get_one_topic(self):
        request, response = app.test_client.get(f'/topic/{CREATED_TOPIC_ID}')
        self.assertEqual(response.status, 200)
        data = json.loads(response.text)
        self.assertEqual(len(data['topics']), 1)

    def test_08_get_one_post(self):
        request, response = app.test_client.get(f'/topic/{CREATED_TOPIC_ID}/post/{CREATED_POST_ID}')
        self.assertEqual(response.status, 200)
        data = json.loads(response.text)
        self.assertTrue(data.get('post') is not None)
        self.assertTrue(data.get('comments') is not None)

    def test_09_update_topic(self):
        data = {
            "subject": f"topic modified {random.randint(0, 100_000_000)}",  # must be unique
            "description": f"topic modified"
        }
        request, response = app.test_client.put(f'/topic/{CREATED_TOPIC_ID}', data=json.dumps(data))
        self.assertEqual(response.status, 200)

    def test_10_update_post(self):
        data = {
            "subject": f"post modified {random.randint(0, 100_000_000)}",  # must be unique
            "description": f"post modified"
        }
        request, response = app.test_client.put(
            f'/topic/{CREATED_TOPIC_ID}/post/{CREATED_POST_ID}', data=json.dumps(data)
        )
        self.assertEqual(response.status, 200)

    def test_11_delete_post(self):  # check cascade
        request, response = app.test_client.delete(
            f'/topic/{CREATED_TOPIC_ID}/post/{CREATED_POST_ID}', data=json.dumps({})
        )
        self.assertEqual(response.status, 200)

    def test_12_delete_topic(self):  # check cascade
        request, response = app.test_client.delete(f'/topic/{CREATED_TOPIC_ID}', data=json.dumps({}))
        self.assertEqual(response.status, 200)

    def test_13_search_post(self):
        request, response = app.test_client.get('/search?posts=modified')
        self.assertEqual(response.status, 200)
        data = json.loads(response.text)
        self.assertTrue(len(data) > 0)

    def test_14_search_topic(self):
        request, response = app.test_client.get('/search?topics=modified')
        self.assertEqual(response.status, 200)
        data = json.loads(response.text)
        self.assertTrue(len(data) > 0)


if __name__ == '__main__':
    unittest.main()
