import sys
import unittest
from unittest.mock import patch
from api.notification_api import PushNotifierAPI
from datetime import datetime

from main import NewspaperAPI as Newspaper



class TestPushNotifierAPI(unittest.TestCase):

    # Test initialization
    def test_initialization(self):
        newspaper = Newspaper(api_key='test_api_key')
        assert isinstance(newspaper.time_updated, datetime)
        assert newspaper.news == {}
        assert newspaper.api_key == 'test_api_key'


    # Test __str__ method
    def test_str_method(self):
        newspaper = Newspaper(api_key='test_api_key')
        newspaper.time_updated = datetime(2024, 10, 24, 12, 0, 0)
        newspaper.news = {'articles': [{'title': 'Sample Article'}, {'title': 'Another Article'}]}
        
        assert str(newspaper) == 'Last update: 2024-10-24 12:00:00, Amount articles: 2'


    def test_update_news(self):
        newspaper = Newspaper()
        newspaper.update_news()
        assert not newspaper.news == {}

