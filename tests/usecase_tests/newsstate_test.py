import unittest
from unittest.mock import patch, MagicMock
from api.news_api.main import NewsAPI  # Importiere die NewsAPI-Klasse
from api.llm_api import LLMApi

class TestNewsAPI(unittest.TestCase):
    
    @patch.object(NewsAPI, 'fetch_top_headlines')  # Mockt fetch_top_headlines
    @patch.object(NewsAPI, 'get_article')  # Mockt get_article
    @patch.object(NewsAPI, 'summarize_article')  # Mockt summarize_article
    def test_read_article(self, mock_summarize, mock_get_article, mock_fetch_headlines):
        # Mock die Rückgabe von fetch_top_headlines
        mock_fetch_headlines.return_value = ["Headline 1", "Headline 2", "Headline 3"]
        
        # Mock die Rückgabe von get_article
        mock_get_article.return_value = ["This is the full content of the article."]

        # Mock die Rückgabe von summarize_article
        mock_summarize.return_value = "This is the summary of the article."

        # Erstelle eine Instanz von NewsAPI
        news_api = NewsAPI()

        # Teste das Abrufen der Überschriften
        headlines = news_api.get_headlines()
        self.assertEqual(headlines, ["Headline 1", "Headline 2", "Headline 3"])

        # Teste das Abrufen des Artikels
        article = news_api.get_article(0)
        self.assertEqual(article, ["This is the full content of the article."])

        # Teste das Zusammenfassen des Artikels
        summary = news_api.summarize_article("This is the full content of the article.")
        self.assertEqual(summary, "This is the summary of the article.")

        # Überprüfe, ob die gemockten Methoden aufgerufen wurden
        mock_fetch_headlines.assert_called_once()
        mock_get_article.assert_called_once_with(0)
        mock_summarize.assert_called_once_with("This is the full content of the article.")
    
    @patch.object(LLMApi, 'get_response')  # Mockt die LLM-API (dies ist eine zusätzliche Möglichkeit, das LLM zu mocken)
    def test_summarize_article_error(self, mock_llm_response):
        # Simuliere einen Fehler bei der LLM-Antwort
        mock_llm_response.side_effect = Exception("Summary error")

        # Erstelle eine Instanz von NewsAPI
        news_api = NewsAPI()

        # Teste die Fehlerbehandlung, wenn das LLM fehlschlägt
        with self.assertRaises(Exception) as context:
            news_api.summarize_article("Some article content")

        self.assertEqual(str(context.exception), "Summary error")

    @patch.object(NewsAPI, 'fetch_top_headlines')
    def test_no_headlines(self, mock_fetch_headlines):
        # Mock die Rückgabe von fetch_top_headlines als leere Liste
        mock_fetch_headlines.return_value = []

        # Erstelle eine Instanz von NewsAPI
        news_api = NewsAPI()

        # Teste das Abrufen der Überschriften, wenn keine vorhanden sind
        headlines = news_api.get_headlines()
        self.assertEqual(headlines, [])

        # Überprüfe, ob die gemockte Methode aufgerufen wurde
        mock_fetch_headlines.assert_called_once()

    @patch.object(NewsAPI, 'get_article')
    def test_invalid_article_index(self, mock_get_article):
        # Mock die Rückgabe von get_article als None
        mock_get_article.return_value = None

        # Erstelle eine Instanz von NewsAPI
        news_api = NewsAPI()

        # Teste das Abrufen eines Artikels mit einem ungültigen Index
        article = news_api.get_article(999)
        self.assertIsNone(article)

        # Überprüfe, ob die gemockte Methode aufgerufen wurde
        mock_get_article.assert_called_once_with(999)

    @patch.object(NewsAPI, 'summarize_article')
    def test_empty_article_summary(self, mock_summarize):
        # Mock die Rückgabe von summarize_article als leere Zeichenkette
        mock_summarize.return_value = ""

        # Erstelle eine Instanz von NewsAPI
        news_api = NewsAPI()

        # Teste das Zusammenfassen eines leeren Artikels
        summary = news_api.summarize_article("")
        self.assertEqual(summary, "")

        # Überprüfe, ob die gemockte Methode aufgerufen wurde
        mock_summarize.assert_called_once_with("")

if __name__ == "__main__":
    unittest.main()
