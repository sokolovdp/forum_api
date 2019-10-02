import json
import unittest
import random

from forum import app

N = random.randint(1, 10000)

CREATED_TOPIC_ID = None
CREATED_POST_ID = None
CREATED_COMMENT_ID = None


class AutoRestTests(unittest.TestCase):
    """ Unit test cases for Forum Rest APIs  """

    def setUp(self):
        pass

    def test_create_topic(self):
        global CREATED_TOPIC_ID

        data = {
            "subject": f"topic {N} subject",
            "description": f"topic {N} description"
        }
        request, response = app.test_client.post('/topic/0', data=json.dumps(data))
        self.assertEqual(response.status, 200)
        data = json.loads(response.text)
        CREATED_TOPIC_ID = int(data['id'])
        print(f'created topic id = {CREATED_TOPIC_ID}')

    def test_create_post(self):
        global CREATED_POST_ID

        data = {
            "subject": f"post {N} subject",
            "description": f"post {N} description"
        }
        request, response = app.test_client.post(f'topic/{CREATED_TOPIC_ID}/post/0', data=json.dumps(data))
        self.assertEqual(response.status, 200)
        data = json.loads(response.text)
        CREATED_POST_ID = int(data['id'])
        print(f'created post id = {CREATED_POST_ID}')

    def test_create_comment(self):
        global CREATED_COMMENT_ID

        data = {
            "text": f"post 1 comment {N}",
            "comment_id": None,
            "topic_id": 1,
            "post_id": 2
        }
        request, response = app.test_client.post('/comment', data=json.dumps(data))
        self.assertEqual(response.status, 200)
        data = json.loads(response.text)
        CREATED_COMMENT_ID = int(data['id'])
        print(f'created comment id = {CREATED_COMMENT_ID}')

    def test_create_comment_for_comment(self):
        data = {
            "text": f"comment for comment {CREATED_COMMENT_ID}",
            "comment_id": CREATED_COMMENT_ID,
            "topic_id": 1,
            "post_id": 2
        }
        request, response = app.test_client.post('/comment', data=json.dumps(data))
        self.assertEqual(response.status, 200)
        data = json.loads(response.text)
        print(f'created comment for comment id = {int(data["id"])}')

    def test_get_list_of_topics(self):
        request, response = app.test_client.get('/topic/0')
        self.assertEqual(response.status, 200)
        data = json.loads(response.text)
        self.assertTrue(data.get('topics') is not None)

    def test_get_list_of_posts(self):
        request, response = app.test_client.get('/topic/1/post/0')
        self.assertEqual(response.status, 200)
        data = json.loads(response.text)
        self.assertTrue(data.get('posts') is not None)

    def test_get_one_topic(self):
        request, response = app.test_client.get('/topic/1')
        self.assertEqual(response.status, 200)
        data = json.loads(response.text)
        self.assertEqual(len(data['topics']), 1)

    def test_get_one_post(self):
        request, response = app.test_client.get('/topic/1/post/2')
        self.assertEqual(response.status, 200)
        data = json.loads(response.text)
        self.assertTrue(data.get('post') is not None)
        self.assertTrue(data.get('comments') is not None)

    def test_update_topic(self):
        data = {
            "subject": f"topic modified",
            "description": f"topic modified"
        }
        request, response = app.test_client.put('/topic/1', data=json.dumps(data))
        self.assertEqual(response.status, 200)

    def test_update_post(self):
        data = {
            "subject": f"post modified",
            "description": f"post modified"
        }
        request, response = app.test_client.put('/topic/1/post/2', data=json.dumps(data))
        self.assertEqual(response.status, 200)

    def test_delete_post(self):  # check cascade
        request, response = app.test_client.delete('/topic/1/post/12', data=json.dumps({}))
        self.assertEqual(response.status, 200)

    def test_delete_topic(self):  # check cascade
        request, response = app.test_client.delete('/topic/15', data=json.dumps({}))
        self.assertEqual(response.status, 200)

    def test_search_post(self):
        request, response = app.test_client.get('/search?posts=modified')
        self.assertEqual(response.status, 200)
        data = json.loads(response.text)
        self.assertTrue(len(data) > 0)

    def test_search_topic(self):
        request, response = app.test_client.get('/search?topics=modified')
        self.assertEqual(response.status, 200)
        data = json.loads(response.text)
        self.assertTrue(len(data) > 0)


if __name__ == '__main__':
    unittest.main()
