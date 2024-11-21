import sys
import unittest
from unittest.mock import patch
from datetime import datetime


from api.news_api.main import NewspaperAPI as Newspaper


class TestNewsAPI(unittest.TestCase):

    # Test initialization
    def test_initialization(self):
        newspaper = Newspaper(api_key='test_api_key')
        self.assert_(isinstance(newspaper.time_updated, datetime))
        self.assertEqual(newspaper.news, {})
        self.assertEqual(newspaper.api_key, 'test_api_key')


    # Test __str__ method
    def test_str_method(self):
        newspaper = Newspaper(api_key='test_api_key')
        newspaper.time_updated = datetime(2024, 10, 24, 12, 0, 0)
        newspaper.news = {'articles': [{'title': 'Sample Article'}, {'title': 'Another Article'}]}
        
        self.assert_(str(newspaper) == 'Last update: 2024-10-24 12:00:00, Amount articles: 2')



    def test_update_news(self):
        newspaper = Newspaper()
        newspaper.update_news()
        self.assert_(not newspaper.news == {})


if __name__ == '__main__':
    unittest.main()