from datetime import datetime
import unittest
from unittest.mock import patch
from api.api_factory.main import APIFactory
from api.weather_api.main import WeatherAPI
from config.config import CONFIG

class TestApiFactory(unittest.TestCase):

    def setUp(self):
        config = {
            'weather_api_key': 'test_key',
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
        self.assertEqual(api.api_key, 'test_api')
    
    # test unsupported api type
    def test_create_unsupported_api(self):
        with self.assertRaises(ValueError):
            self.factory.create_api('maps')