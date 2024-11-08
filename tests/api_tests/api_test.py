import unittest
from unittest.mock import patch
from api.api_factory.main import APIFactory
from api.weather_api.main import WeatherAPI
from config.config import CONFIG

class TestApiFactory(unittest.TestCase):

    def setUp(self):
        config = {
            'weather_api_key': 'test_key',
            'finance_api_key': 'test_key2',
            'fitbit_client_id': 'test_id1',
            'fitbit_client_secret': 'test_secret1'
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
    
    # test unsupported api type
    def test_create_unsupported_api(self):
        with self.assertRaises(ValueError):
            self.factory.create_api('maps')

    # test fitbit api creation
    def test_create_fitbit_api(self):
        api = self.factory.create_api('fitbit')
        self.assertEqual(api.client_id, 'test_id1')
        self.assertEqual(api.client_secret, 'test_secret1')
        
        
class TestWeatherAPI(unittest.TestCase):

    def setUp(self):
        # load 
        
        self.api = WeatherAPI(CONFIG['weather_api_key'])
        
    # Test weather API URL
    def test_api_url(self):
        self.assertEqual(self.api.base_url, 'https://api.openweathermap.org/data/2.5')
    
    # Test get_weather method with mock response
    @patch('api.weather_api.main.APIClient.get')
    def test_get_weather(self, mock_get):
        # Set up the mock to return a specific response
        mock_get.return_value = {
            'main': {
                'temp': 15,
                'humidity': 70
            },
            'weather': [{'description': 'clear sky'}]
        }
        
        # Call the method under test
        response = self.api.get_weather('London', 'metric')
        
        # Assert the response matches the mock
        self.assertEqual(response['main']['temp'], 15)
        self.assertEqual(response['main']['humidity'], 70)
        self.assertEqual(response['weather'][0]['description'], 'clear sky')

if __name__ == '__main__':
    unittest.main()