import os
import json
import unittest
import random

from sqlalchemy import create_engine

from forum import app
import tables


class AutoRestTests(unittest.TestCase):
    """ Unit test cases for Forum Rest APIs  """

    def setUp(self):
        pass

    def test_create_topic(self):
        n = random.randint(1, 10000)
        data = {
            "subject": f"topic {n}",
            "description": f"topic {n} description"
        }
        request, response = app.test_client.post('/topic/0', data=json.dumps(data))
        self.assertEqual(response.status, 200)

    def test_create_post(self):
        n = random.randint(1, 10000)
        data = {
            "subject": f"post {n}",
            "description": f"post {n} description"
        }
        request, response = app.test_client.post('topic/1/post/0', data=json.dumps(data))
        self.assertEqual(response.status, 200)

    def test_create_comment(self):
        n = random.randint(1, 10000)
        data = {
            "text": f"post 1 comment {n}",
            "comment_id": None,
            "topic_id": 1,
            "post_id": 2
        }
        request, response = app.test_client.post('/comment', data=json.dumps(data))
        self.assertEqual(response.status, 200)

    def test_create_comment_for_comment(self):
        n = random.randint(1, 10000)
        data = {
            "text": f"comment for comment {n}",
            "comment_id": 10,
            "topic_id": 1,
            "post_id": 2
        }
        request, response = app.test_client.post('/comment', data=json.dumps(data))
        self.assertEqual(response.status, 200)

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
        pass

    def test_update_post(self):
        pass

    def test_delete_post(self):
        pass

    def test_delete_topic(self):   # check cascade
        pass

    def test_search_post(self):
        pass

    def test_search_topic(self):
        pass


if __name__ == '__main__':
    unittest.main()
