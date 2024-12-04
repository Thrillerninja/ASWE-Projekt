from unittest.mock import patch, MagicMock
from newsapi.newsapi_client import NewsApiClient
import unittest
from api.news_api.main import NewsAPI


class TestNewsAPI(unittest.TestCase):

    @patch("api.llm_api.LLMApi.get_response")  # Patch der get_response Methode direkt
    def test_summarize_article(self, mock_get_response):
        # Setze die Rückgabe der gemockten get_response-Methode
        mock_get_response.return_value = "Summary of the article"

        # Erstelle eine Instanz von NewsAPI
        news_api = NewsAPI()

        # Rufe die zu testende Methode auf
        result = news_api.summarize_article("Some article content")

        # Überprüfe, ob das Ergebnis mit der erwarteten Zusammenfassung übereinstimmt
        self.assertEqual(result, "Summary of the article")

        # Überprüfe, ob get_response mit den richtigen Parametern aufgerufen wurde
        mock_get_response.assert_called_with(
            model="llama3.2:1b",
            message_content="Fasse diesn Artikel in 1-4 Sätzen auf deutsch zusammen. Verwende keine Sonderzeichen:\nSome article content",
        )


    @patch('newsapi.newsapi_client.NewsApiClient.get_top_headlines')  # Mocke den `client`
    def test_fetch_top_headlines_success(self, mock_client):
        # Simulierte API-Antwort
        mock_client.return_value = {
            'status': 'ok',
            'articles': [
                {'title': '5 &gt; 1', 'description': 'Eine Beschreibung'}
            ]
        }
        fetcher = NewsAPI()
        fetcher.source = 'test-source'  # Beispiel-Quelle
        articles = fetcher.fetch_top_headlines()
        # Überprüfe das Ergebnis
        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0]['title'], '5 > 1')  # HTML-Dekodiert
        mock_client.assert_called_with(language='de', sources='test-source')

        mock_client.return_value = {
            'status': 'nicht ok',
            'articles': [
                {'title': 'new article', 'description': 'new description'}
            ]
        }
        articles = fetcher.fetch_top_headlines()
        self.assertIsNot(articles, mock_client.return_value)



    @patch('requests.get')
    def test_get_article(self, mock_client):
        # Simulierte API-Antwort
        class MockResponse:
            def __init__(self, status_code, text):
                self.status_code = status_code
                self.text = text

        mock_client.return_value = MockResponse(69420, '-')
        fetcher = NewsAPI()
        article = fetcher.get_article('invalid-url')
        self.assertIsNone(article)

        mock_client.return_value = MockResponse(200, "line1\nline2")
        article = fetcher.get_article('invalid-url')
        self.assertIsNone(article)


        mock_client.return_value = MockResponse(200, "line1\n\"articleBody\": 5&gt;1\nline2")
        article = fetcher.get_article('invalid-url')
        self.assertEqual(article, '5>1')
