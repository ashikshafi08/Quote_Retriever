import unittest
import json
import argparse
from app import app

class TestFlaskApi(unittest.TestCase):
    query = "default"

    @classmethod
    def setUpClass(cls):
        parser = argparse.ArgumentParser(description='Test the search API with a query.')
        parser.add_argument('--query', type=str, default=cls.query, help='Query to search for')
        args = parser.parse_args()
        cls.query = args.query

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_get_search_no_query(self):
        response = self.app.get('/search')
        self.assertEqual(response.status_code, 400)

    def test_get_search_with_query(self):
        response = self.app.get(f'/search?query={self.query}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertIsInstance(data, list)

if __name__ == '__main__':
    unittest.main()
