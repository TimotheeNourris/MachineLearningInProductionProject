import unittest
from app import app

class FlaskTest(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        
    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1>Entrez les informations du film</h1>', response.data)
        
    def test_submit(self):
        data = {
            'title': 'My Anime',
            'genre': "['Action', 'Fantasy']",
            'synopsis': 'An exciting anime',
            'type': 'TV',
            'producer': "['Dwango']",
            'studio': "['Madhouse']"
        }
        response = self.app.post('/submit', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1>Informations soumises avec succes</h1>', response.data)

if __name__ == '__main__':
    unittest.main()
