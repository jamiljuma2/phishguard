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
        # Missing 'type'
        response2 = self.app.post('/predict', json={"text": "test"})
        self.assertEqual(response2.status_code, 400)
        # Missing 'text'
        response3 = self.app.post('/predict', json={"type": "email"})
        self.assertEqual(response3.status_code, 400)

    def test_predict_email(self):
        response = self.app.post('/predict', json={"text": "This is a test email about your account. Click here to login.", "type": "email"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.is_json)
        data = response.get_json()
        self.assertIn('result', data)
        self.assertIn('confidence', data)
        self.assertIn('heuristics', data)

    def test_predict_sms(self):
        response = self.app.post('/predict', json={"text": "URGENT: Your bank account is locked. Visit http://phish.com", "type": "sms"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.is_json)
        data = response.get_json()
        self.assertIn('result', data)
        self.assertIn('confidence', data)
        self.assertIn('heuristics', data)

    def test_predict_url(self):
        response = self.app.post('/predict', json={"text": "http://malicious-url.com/reset-password", "type": "url"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.is_json)
        data = response.get_json()
        self.assertIn('result', data)
        self.assertIn('confidence', data)
        self.assertIn('heuristics', data)

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
