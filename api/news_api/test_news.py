from datetime import datetime
from API.news_api.main import NewspaperAPI as Newspaper


# Test initialization
def test_initialization():
    newspaper = Newspaper(api_key='test_api_key')
    assert isinstance(newspaper.time_updated, datetime)
    assert newspaper.news == {}
    assert newspaper.api_key == 'test_api_key'


# Test __str__ method
def test_str_method():
    newspaper = Newspaper(api_key='test_api_key')
    newspaper.time_updated = datetime(2024, 10, 24, 12, 0, 0)
    newspaper.news = {'articles': [{'title': 'Sample Article'}, {'title': 'Another Article'}]}
    
    expected_str = 'Last update: 2024-10-24 12:00:00, Amount articles: 2'
    assert str(newspaper) == expected_str

