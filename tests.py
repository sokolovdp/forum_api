import json
import unittest
import random

from forum import app


class ForumTests(unittest.TestCase):
    """ Unit test cases for Forum Rest APIs  """
    N = random.randint(1, 10000)
    CREATED_TOPIC_ID = None
    CREATED_POST_ID = None
    CREATED_COMMENT_ID = None

    def setUp(self):
        pass

    def test_01_create_topic(self):
        data = {
            "subject": f"topic {self.__class__.N} subject",
            "description": f"topic {self.__class__.N} description"
        }
        request, response = app.test_client.post('/topic/0', data=json.dumps(data))
        self.assertEqual(response.status, 200)
        data = json.loads(response.text)
        self.__class__.CREATED_TOPIC_ID = int(data['id'])

    def test_02_create_post(self):
        data = {
            "subject": f"post {self.__class__.N} subject",
            "description": f"post {self.__class__.N} description"
        }
        request, response = app.test_client.post(
            f'topic/{self.__class__.CREATED_TOPIC_ID}/post/0', data=json.dumps(data)
        )
        self.assertEqual(response.status, 200)
        data = json.loads(response.text)
        self.__class__.CREATED_POST_ID = int(data['id'])

    def test_03_create_comment(self):
        data = {
            "text": f"post {self.__class__.CREATED_POST_ID} comment {self.__class__.N}",
            "comment_id": None,
            "topic_id": self.__class__.CREATED_TOPIC_ID,
            "post_id": self.__class__.CREATED_POST_ID
        }
        request, response = app.test_client.post('/comment', data=json.dumps(data))
        self.assertEqual(response.status, 200)
        data = json.loads(response.text)
        self.__class__.CREATED_COMMENT_ID = int(data['id'])

    def test_04_create_comment_for_comment(self):
        data = {
            "text": f"comment for comment {self.__class__.CREATED_COMMENT_ID}",
            "comment_id": self.__class__.CREATED_COMMENT_ID,
            "topic_id": self.__class__.CREATED_TOPIC_ID,
            "post_id": self.__class__.CREATED_POST_ID
        }
        request, response = app.test_client.post('/comment', data=json.dumps(data))
        self.assertEqual(response.status, 200)

    def test_05_get_list_of_topics(self):
        request, response = app.test_client.get('/topic/0')
        self.assertEqual(response.status, 200)
        data = json.loads(response.text)
        topic_list = data.get('topics')
        self.assertTrue(topic_list is not None)
        self.assertTrue(len(topic_list) > 0)

    def test_06_get_list_of_posts(self):
        request, response = app.test_client.get(f'/topic/{self.__class__.CREATED_TOPIC_ID}/post/0')
        self.assertEqual(response.status, 200)
        data = json.loads(response.text)
        post_list = data.get('posts')
        self.assertTrue(post_list is not None)
        self.assertTrue(len(post_list) > 0)

    def test_07_get_one_topic(self):
        request, response = app.test_client.get(f'/topic/{self.__class__.CREATED_TOPIC_ID}')
        self.assertEqual(response.status, 200)
        data = json.loads(response.text)
        self.assertEqual(len(data['topics']), 1)

    def test_08_get_one_post(self):
        request, response = app.test_client.get(
            f'/topic/{self.__class__.CREATED_TOPIC_ID}/post/{self.__class__.CREATED_POST_ID}'
        )
        self.assertEqual(response.status, 200)
        data = json.loads(response.text)
        self.assertTrue(data.get('post') is not None)
        self.assertTrue(data.get('comments') is not None)

    def test_09_update_topic(self):
        data = {
            "subject": f"topic {self.__class__.N} modified {random.randint(0, 100_000_000)}",  # unique
            "description": f"topic modified"
        }
        request, response = app.test_client.put(
            f'/topic/{self.__class__.CREATED_TOPIC_ID}', data=json.dumps(data)
        )
        self.assertEqual(response.status, 200)

    def test_10_update_post(self):
        data = {
            "subject": f"post {self.__class__.N} modified {random.randint(0, 100_000_000)}",  # unique
            "description": f"post modified"
        }
        request, response = app.test_client.put(
            f'/topic/{self.__class__.CREATED_TOPIC_ID}/post/{self.__class__.CREATED_POST_ID}',
            data=json.dumps(data)
        )
        self.assertEqual(response.status, 200)

    def test_11_search_post(self):
        request, response = app.test_client.get(f'/search?posts={self.__class__.N}')
        self.assertEqual(response.status, 200)
        data = json.loads(response.text)
        self.assertTrue(len(data) > 0)

    def test_12_search_topic(self):
        request, response = app.test_client.get(f'/search?topics={self.__class__.N}')
        self.assertEqual(response.status, 200)
        data = json.loads(response.text)
        self.assertTrue(len(data) > 0)

    def test_13_delete_post(self):
        request, response = app.test_client.delete(
            f'/topic/{self.__class__.CREATED_TOPIC_ID}/post/{self.__class__.CREATED_POST_ID}',
        )
        self.assertEqual(response.status, 200)

    def test_14_delete_topic(self):
        request, response = app.test_client.delete(f'/topic/{self.__class__.CREATED_TOPIC_ID}')
        self.assertEqual(response.status, 200)


if __name__ == '__main__':
    unittest.main()
