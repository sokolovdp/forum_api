import json
import unittest

from forum import app


class AutoRestTests(unittest.TestCase):
    """ Unit test cases for Forum Rest APIs  """

    def test_get_list_of_topics(self):
        request, response = app.test_client.get('/topic/0')
        self.assertEqual(response.status, 200)
        data = json.loads(response.text)
        self.assertEqual(len(data['topics']), 2)


if __name__ == '__main__':
    unittest.main()
