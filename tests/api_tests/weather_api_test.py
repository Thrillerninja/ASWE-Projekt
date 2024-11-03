import datetime
import unittest
from unittest.mock import patch, MagicMock
from api.weather_api.main import WeatherAPI
from config.config import CONFIG

CLEAR_SKY = 'clear sky'

class TestWeatherAPI(unittest.TestCase):

    def setUp(self):
        self.api = WeatherAPI(CONFIG['weather_api_key'])

    # Test weather API URL
    def test_api_url(self):
        self.assertEqual(self.api.base_url, 'https://api.openweathermap.org')

    # Test get_weather method with mock response
    @patch('api.weather_api.main.APIClient.get')
    def test_get_weather(self, mock_get):
        # Set up the mock to return a specific response
        mock_get.return_value = {
            'main': {
                'temp': 15,
            'weather': [{'description': CLEAR_SKY}]
            },
            'weather': [{'description': CLEAR_SKY}]
        }

        # Call the method under test
        response = self.api.get_weather('London', 'metric')

        # Assert the response matches the mock
        self.assertEqual(response['weather'][0]['description'], CLEAR_SKY)
        self.assertEqual(response['main']['temp'], 15)

    @patch('api.weather_api.main.APIClient.get')
    def test_get_forecast(self, mock_get):
        # Set up the mock to return a specific response
        mock_get.return_value = {
            'list': [
                {
                    'dt_txt': '2021-01-01 12:00:00',
                    'main': {
                        'temp_min': 10,
                        'temp_max': 20
                    },
                    'weather': [{'description': CLEAR_SKY}]
                }
            ]
        }

        # Call the method under test
        response = self.api.get_forecast('London', 'metric')

        # Assert the response matches the mock
        self.assertEqual(response['list'][0]['weather'][0]['description'], CLEAR_SKY)
        self.assertEqual(response['list'][0]['main']['temp_max'], 20)

    @patch('api.weather_api.main.WeatherAPI.get_forecast')
    def test_get_formatted_forecast(self, mock_get_forecast):
        # Set up the mock to return a specific response
        mock_get_forecast.return_value = {
            'list': [
                {
                    'dt_txt': '2021-01-01 12:00:00',
                    'main': {
                        'temp_min': 10,
                        'temp_max': 20
                    },
                    'weather': [{'description': CLEAR_SKY}]
                }
            ]
        }

        # Call the method under test
        response = self.api.get_formatted_forecast('London', 'metric')
        self.assertEqual(response, f'Aktuelles Wetter10°C to 20°C, {CLEAR_SKY} Heute Mittag10°C to 20°C, {CLEAR_SKY}')
        # Assert the response matches the expected format
        self.assertEqual(response, 'Aktuelles Wetter10°C to 20°C, clear sky Heute Mittag10°C to 20°C, clear sky')

    @patch('api.weather_api.main.WeatherAPI.get_forecast')
    def test_get_daily_forecast(self, mock_get_forecast):
        # Set up the mock to return a specific response
        mock_get_forecast.return_value = {
            'list': [
                {
                    'dt_txt': '2021-01-01 12:00:00',
                    'main': {
                        'temp_min': 10,
                        'temp_max': 20,
                        'temp': 15
                    },
                    'weather': [{'description': CLEAR_SKY}]
                }
            ]
        }

        # Call the method under test
        response = self.api.get_daily_forecast('London', datetime.datetime.strptime('2021-01-01', '%Y-%m-%d'))

        # Assert the response matches the mock
        self.assertEqual(response['min_temp'], 10)
        self.assertEqual(response['avg_condition'], CLEAR_SKY)
        self.assertEqual(response['avg_temp'], 15)

    @patch('api.weather_api.main.APIClient.get')
    def test_get_city_coords(self, mock_get):
        # Set up the mock to return a specific response
        mock_get.return_value = [
            {
                'lat': 51.51,
                'lon': -0.13
            }
        ]

        # Call the method under test
        response = self.api.get_city_coords('London')

        # Assert the response matches the mock
        self.assertEqual(response['lat'], 51.51)
        self.assertEqual(response['lon'], -0.13)
