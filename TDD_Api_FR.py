from app import *
from resources.db_func import Database
import unittest

app.testing= True

class APITests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_get_metrics(self):
        response = self.app.get("/metrics?last_quotes=1")
        self.assertEqual(200, response.status_code)

if __name__ == "__main__":
    db = Database()
    unittest.main()