import unittest
from unittest.mock import patch
from api.api_factory import APIFactory
from api.calendar_api import RaplaAPI
from api.weather_api import WeatherAPI
from config.config import CONFIG

class TestApiFactory(unittest.TestCase):

    def setUp(self):
        config = {'weather_api_key': 'test_key'}
        self.factory = APIFactory(config)

    # test weather api creation
    def test_create_weather_api(self):
        api = self.factory.create_api('weather')
        self.assertEqual(api.api_key, 'test_key')
    
    # test unsupported api type
    def test_create_unsupported_api(self):
        with self.assertRaises(ValueError):
            self.factory.create_api('maps')
        
        
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
        
        
class TestRaplaAPI(unittest.TestCase):
        
    def test_create_rapla_api(self):
        api = RaplaAPI(22, 'A')
        self.assertEqual(api.url, 'https://rapla.dhbw.de/rapla/internal_calendar?user=doelker%40verwaltung.ba-stuttgart.de&file=22A&day=30&month=9&year=2024&pages=20')
        self.assertIsNotNone(api.calendar)
        
    def test_create_rapla_api_no_calendar(self):
        api = RaplaAPI(22, 'Z')
        self.assertEqual(api.url, 'https://rapla.dhbw.de/rapla/internal_calendar?user=doelker%40verwaltung.ba-stuttgart.de&file=22Z&day=30&month=9&year=2024&pages=20')
        self.assertIsNone(api.calendar)
        
    def test_create_rapla_api_with_invalid_email(self):
        api = RaplaAPI(22, 'A', 'test@example.com')
        self.assertEqual(api.url, 'https://rapla.dhbw.de/rapla/internal_calendar?user=test%40example.com&file=22A&day=30&month=9&year=2024&pages=20')
        self.assertIsNone(api.calendar)
        
    def test_create_rapla_api_with_email_no_calendar(self):
        api = RaplaAPI(22, 'Z', 'test@example.com')
        self.assertEqual(api.url, 'https://rapla.dhbw.de/rapla/internal_calendar?user=test%40example.com&file=22Z&day=30&month=9&year=2024&pages=20')
        self.assertIsNone(api.calendar)
        
if __name__ == '__main__':
    unittest.main()