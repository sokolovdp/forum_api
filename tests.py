import json
import unittest

from forum import app


class AutoRestTests(unittest.TestCase):
    """ Unit test cases for Forum Rest APIs  """

    def test_create_topic(self):
        pass

    def test_create_post(self):
        pass

    def test_create_comment(self):
        pass

    def test_create_comment_for_comment(self):
        pass

    def test_get_list_of_topics(self):
        request, response = app.test_client.get('/topic/0')
        self.assertEqual(response.status, 200)
        data = json.loads(response.text)
        self.assertEqual(len(data['topics']), 2)

    def test_get_list_of_posts(self):
        pass

    def test_get_one_topic(self):
        request, response = app.test_client.get('/topic/1')
        self.assertEqual(response.status, 200)
        data = json.loads(response.text)
        self.assertEqual(len(data['topics']), 1)

    def test_get_one_post(self):
        pass

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
