import sys
from app import *
from resources.db_func import Database
import unittest

app.testing= True
db = Database()
class APITests(unittest.TestCase):
    db = Database()
    def setUp(self):
        self.app = app.test_client()
        db = Database()

    def test_get_metrics(self):
        db = Database()
        response = self.app.get("/metrics")
        self.assertEqual(200, response.status_code)

if __name__ == "__main__":
    db = Database()
    unittest.main()