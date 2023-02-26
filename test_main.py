import unittest
from app import app
import json

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_prediction(self):
        input_data = {
            'Title': 'a',
            'Genre': ['Action', 'Space', 'Drama', 'Mystery'],
            'Description': 'a',
            'Type': 'TV',
            'Producer': "['Victor Entertainment']",
            'Studio': "['Lide']"
        }

        response = self.app.get('/', data=input_data)

        # check if the response is successful
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
