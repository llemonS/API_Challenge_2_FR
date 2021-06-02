from app import *
import unittest

app.testing= True

class APITests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_get_metrics(self):
        response = self.app.get("/metrics")
        self.assertEqual(200, response.status_code)

if __name__ == "__main__":
    unittest.main()