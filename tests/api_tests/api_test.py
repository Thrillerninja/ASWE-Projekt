from datetime import datetime
import unittest
from unittest.mock import patch, MagicMock
from api.api_factory.main import APIFactory
from api.weather_api.main import WeatherAPI
from api.api_client import APIClient
from config.config import CONFIG

class TestApiFactory(unittest.TestCase):

    def setUp(self):
        config = {
            'weather_api_key': 'test_key',
            'finance_api_key': 'test_key2',
            'spotify_client_id': 'test_key3',
            'spotify_client_secret': 'test_key4'
            'finance_api_key': 'test_api'
            }
        self.factory = APIFactory(config)

    # test weather api creation
    def test_create_weather_api(self):
        api = self.factory.create_api('weather')
        self.assertEqual(api.api_key, 'test_key')
        
    # test finance api creation
    def test_create_finance_api(self):
        api = self.factory.create_api('finance')
        self.assertEqual(api.api_key, 'test_key2')

    # test spotify api creation
    def test_create_finance_api(self):
        api = self.factory.create_api('spotify')
        self.assertEqual(api.client_id, 'test_key3')
        self.assertEqual(api.client_secret, 'test_key4')
        self.assertEqual(api.api_key, 'test_api')
    
    # test unsupported api type
    def test_create_unsupported_api(self):
        with self.assertRaises(ValueError):
            self.factory.create_api('maps')
            

class TestableAPIClient(APIClient):
    def authenticate(self):
        pass  # No authentication needed for testing

class TestApiClient(unittest.TestCase):

    def setUp(self):
        self.base_url = 'https://api.example.com'
        self.headers = {'Authorization': 'Bearer test_token'}
        self.client = TestableAPIClient(self.base_url, self.headers)

    @patch('requests.get')
    def test_get(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {'key': 'value'}
        mock_get.return_value = mock_response

        response = self.client.get('endpoint')
        self.assertEqual(response, {'key': 'value'})
        mock_get.assert_called_once_with(f'{self.base_url}/endpoint', headers=self.headers, params=None)

    @patch('requests.post')
    def test_post(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {'key': 'value'}
        mock_post.return_value = mock_response

        response = self.client.post('endpoint', json={'data': 'value'})
        self.assertEqual(response, {'key': 'value'})
        mock_post.assert_called_once_with(f'{self.base_url}/endpoint', headers=self.headers, data=None, json={'data': 'value'})

    @patch('requests.put')
    def test_put(self, mock_put):
        mock_response = MagicMock()
        mock_response.json.return_value = {'key': 'value'}
        mock_put.return_value = mock_response

        response = self.client.put('endpoint', data={'data': 'value'})
        self.assertEqual(response, {'key': 'value'})
        mock_put.assert_called_once_with(f'{self.base_url}/endpoint', headers=self.headers, data={'data': 'value'})

    @patch('requests.delete')
    def test_delete(self, mock_delete):
        mock_response = MagicMock()
        mock_response.json.return_value = {'key': 'value'}
        mock_delete.return_value = mock_response

        response = self.client.delete('endpoint')
        self.assertEqual(response, {'key': 'value'})
        mock_delete.assert_called_once_with(f'{self.base_url}/endpoint', headers=self.headers)

if __name__ == '__main__':
    unittest.main()