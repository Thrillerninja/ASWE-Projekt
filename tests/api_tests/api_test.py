import sys
from loguru import logger
from datetime import datetime
import unittest
from unittest.mock import patch, MagicMock
from api.api_factory.main import APIFactory
from api.weather_api.main import WeatherAPI
from api.api_client import APIClient
from config.config import CONFIG

class TestApiFactory(unittest.TestCase):

    def setUp(self):
        logger.info("Setting up TestApiFactory")
        config = {
            'weather_api_key': 'test_key',
            'finance_api_key': 'test_key',
            'spotify_client_id': 'test_key3',
            'spotify_client_secret': 'test_key4',
            'fitbit_client_id': 'test_key5',
            'fitbit_client_secret': 'test_key6'
            }
        self.factory = APIFactory(config)

    # test weather api creation
    def test_create_weather_api(self):
        logger.info("Testing weather API creation")
        api = self.factory.create_api('weather')
        self.assertEqual(api.api_key, 'test_key')
        
    # test finance api creation
    def test_create_finance_api(self):
        logger.info("Testing finance API creation")
        api = self.factory.create_api('finance')
        self.assertEqual(api.api_key, 'test_key')

    # test spotify api creation
    @patch('api.spotify_api.main.SpotifyAPI.update_token')
    def test_create_spotify_api(self, mock_update_token):
        logger.info("Testing Spotify API creation")
        mock_update_token.return_value = None  # Assuming update_token does not return anything
        self.factory.create_api('spotify')
        mock_update_token.assert_called_once()
    
    # test unsupported api type
    def test_create_unsupported_api(self):
        logger.info("Testing unsupported API creation")
        with self.assertRaises(ValueError):
            self.factory.create_api('maps')
    
    # test fitbit api creation
    def test_create_fitbit_api(self):
        api = self.factory.create_api('fitbit')
        self.assertEqual(api.client_id, 'test_key5')
        self.assertEqual(api.client_secret, 'test_key6')
            

class TestableAPIClient(APIClient):
    def authenticate(self):
        pass  # No authentication needed for testing

class TestApiClient(unittest.TestCase):

    def setUp(self):
        logger.info("Setting up TestApiClient")
        self.base_url = 'https://api.example.com'
        self.headers = {'Authorization': 'Bearer test_token'}
        self.client = TestableAPIClient(self.base_url, self.headers)

    @patch('requests.get')
    def test_get(self, mock_get):
        logger.info("Testing GET request")
        mock_response = MagicMock()
        mock_response.json.return_value = {'key': 'value'}
        mock_get.return_value = mock_response

        response = self.client.get('endpoint')
        self.assertEqual(response, {'key': 'value'})
        mock_get.assert_called_once_with(f'{self.base_url}/endpoint', headers=self.headers, params=None)

    @patch('requests.post')
    def test_post(self, mock_post):
        logger.info("Testing POST request")
        mock_response = MagicMock()
        mock_response.json.return_value = {'key': 'value'}
        mock_post.return_value = mock_response

        response = self.client.post('endpoint', json={'data': 'value'})
        self.assertEqual(response, {'key': 'value'})
        mock_post.assert_called_once_with(f'{self.base_url}/endpoint', headers=self.headers, data=None, json={'data': 'value'})

    @patch('requests.put')
    def test_put(self, mock_put):
        logger.info("Testing PUT request")
        mock_response = MagicMock()
        mock_response.json.return_value = {'key': 'value'}
        mock_put.return_value = mock_response

        response = self.client.put('endpoint', data={'data': 'value'})
        self.assertEqual(response, {'key': 'value'})
        mock_put.assert_called_once_with(f'{self.base_url}/endpoint', headers=self.headers, data={'data': 'value'})

    @patch('requests.delete')
    def test_delete(self, mock_delete):
        logger.info("Testing DELETE request")
        mock_response = MagicMock()
        mock_response.json.return_value = {'key': 'value'}
        mock_delete.return_value = mock_response

        response = self.client.delete('endpoint')
        self.assertEqual(response, {'key': 'value'})
        mock_delete.assert_called_once_with(f'{self.base_url}/endpoint', headers=self.headers)

if __name__ == '__main__':
    logger.add(sys.stderr, format="{time} | {level} | {name}:{function}:{line} - {message}", level="INFO")
    unittest.main()