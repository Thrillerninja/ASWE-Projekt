# from api.api_client import APIClient
from newsapi import NewsApiClient
import json
from datetime import datetime, timedelta


class NewspaperAPI():
    """
    API client for getting latest news.
    """
    def __init__(self, api_key="ee9ebbc8037b49a58370ee1446c8f8db"):
        self.time_updated = datetime.now()
        self.news = {}
        self.api_key = api_key
        self.newsapi = NewsApiClient(api_key=self.api_key)


    def update_news(self):
        yesterday = (datetime.now()-timedelta(days=1)).strftime('%Y-%m-%d')
        today = datetime.now().strftime('%Y-%m-%d')
        self.news = self.newsapi.get_everything(language='de', sources='die-zeit', sort_by='relevancy', from_param=yesterday, to=today)
        self.time_updated = datetime.now()

    
    def save(self, file='news.json'):
        json.dump(self.news, open(file, 'w', encoding='utf-8'), ensure_ascii=False, indent=4)


    def __str__(self):
        amount_articles = len(self.news.get('articles')) if self.news.get('articles') else 0
        return f'Last update: {self.time_updated.strftime("%Y-%m-%d %H:%M:%S")}, Amount articles: {amount_articles}'

