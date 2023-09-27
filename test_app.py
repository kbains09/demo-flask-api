import unittest
from app import app

class TestCurrencyConverterAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_convert_currency(self):
        response = self.app.get('/convert?from=USD&to=EUR&amount=100')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIn('from', data)
        self.assertIn('to', data)
        self.assertIn('amount', data)
        self.assertIn('converted_amount', data)

    def test_invalid_input(self):
        response = self.app.get('/convert?from=USD&to=EUR')
        data = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', data)

    def test_get_supported_currencies(self):
        response = self.app.get('/currencies')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIn('currencies', data)

if __name__ == '__main__':
    unittest.main()
