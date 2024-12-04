from unittest.mock import patch
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

    @patch('newsapi.newsapi_client.NewsApiClient')  # Mocke den `client`
    def test_fetch_top_headlines_success(self, mock_client):
        # Simulierte API-Antwort
        mock_client.fetch_top_headlines.return_value = {
            'status': 'ok',
            'articles': [
                {'title': 'Nachrichten & Überschriften', 'description': 'Eine Beschreibung'}
            ]
        }

        fetcher = NewsAPI()
        fetcher.source = 'test-source'  # Beispiel-Quelle
        articles = fetcher.fetch_top_headlines()

        # Überprüfe das Ergebnis
        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0]['title'], 'Nachrichten & Überschriften')  # HTML-Dekodiert
        mock_client.fetch_top_headlines.assert_called_with(language='de', sources='test-source')

    @patch('newsapi.newsapi_client.NewsApiClient')  # Mocke den `client`
    def test_fetch_top_headlines_empty(self, mock_client):
        # Simuliere leere Artikel
        mock_client.fetch_top_headlines.return_value = {
            'status': 'ok',
            'articles': []
        }

        fetcher = NewsAPI()
        fetcher.source = 'test-source'
        articles = fetcher.fetch_top_headlines()

        # Überprüfe das Ergebnis
        self.assertEqual(len(articles), 0)

    @patch('newsapi.newsapi_client.NewsApiClient')  # Mocke den `client`
    def test_fetch_top_headlines_failure(self, mock_client):
        # Simuliere API-Fehler
        mock_client.fetch_top_headlines.return_value = {
            'status': 'error',
            'message': 'API Limit exceeded'
        }

        fetcher = NewsAPI()
        fetcher.source = 'test-source'
        articles = fetcher.fetch_top_headlines()

        # Überprüfe, dass `articles` nicht gesetzt wurde
        self.assertIsNone(fetcher.articles)

    @patch('newsapi.newsapi_client.NewsApiClient')  # Mocke den `client`
    def test_fetch_top_headlines_html_escaped(self, mock_client):
        # Simuliere HTML-escapten Titel
        mock_client.fetch_top_headlines.return_value = {
            'status': 'ok',
            'articles': [
                {'title': 'Nachrichten &amp; Überschriften'}
            ]
        }

        fetcher = NewsAPI()
        fetcher.source = 'test-source'
        articles = fetcher.fetch_top_headlines()

        # Überprüfe HTML-Unescaping
        self.assertEqual(articles[0]['title'], 'Nachrichten & Überschriften')

    @patch('article.requests.get')  # Mocke requests.get
    def test_get_article_success(self, mock_get):
        # Simulierte HTTP-Antwort
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = (
            '\n'
            '...other content...\n'
            '  "articleBody": "This is a test article &amp; it is great!©source dpa"\n'
            '...other content...\n'
        )

        fetcher = ArticleFetcher()
        url = "http://example.com/article"
        result = fetcher.get_article(url)

        # Überprüfe das Ergebnis
        self.assertEqual(result, "This is a test article & it is great!")

    @patch('article.requests.get')  # Mocke requests.get
    def test_get_article_no_article_body(self, mock_get):
        # Simuliere HTTP-Antwort ohne "articleBody"
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = (
            '\n'
            '...other content...\n'
            '  "someOtherField": "No article body here."\n'
            '...other content...\n'
        )

        fetcher = ArticleFetcher()
        url = "http://example.com/article"
        result = fetcher.get_article(url)

        # Überprüfe, dass None zurückgegeben wird
        self.assertIsNone(result)

    @patch('article.requests.get')  # Mocke requests.get
    def test_get_article_http_failure(self, mock_get):
        # Simuliere einen HTTP-Fehler
        mock_get.return_value.status_code = 404

        fetcher = ArticleFetcher()
        url = "http://example.com/article"
        result = fetcher.get_article(url)

        # Überprüfe, dass None zurückgegeben wird
        self.assertIsNone(result)

    @patch('article.requests.get')  # Mocke requests.get
    def test_get_article_invalid_format(self, mock_get):
        # Simuliere eine Antwort ohne korrekt formatierten JSON-ähnlichen Inhalt
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = (
            '\n'
            '...other content...\n'
            '  "articleBody": "Unclosed string starts here...\n'
        )

        fetcher = ArticleFetcher()
        url = "http://example.com/article"
        result = fetcher.get_article(url)

        # Überprüfe, dass None zurückgegeben wird
        self.assertIsNone(result)