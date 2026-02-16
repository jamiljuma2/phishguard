import unittest
from app import app

class BackendApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_health(self):
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'healthy', response.data)

    def test_predict_missing_fields(self):
        response = self.app.post('/predict', json={})
        self.assertEqual(response.status_code, 400)

    def test_history(self):
        response = self.app.get('/history')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.is_json)

    def test_dashboard_stats(self):
        response = self.app.get('/dashboard_stats')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.is_json)

if __name__ == '__main__':
    unittest.main()
