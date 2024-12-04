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
