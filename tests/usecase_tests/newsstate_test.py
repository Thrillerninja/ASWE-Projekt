import unittest
from unittest.mock import MagicMock, patch, call
from usecases.news_state import NewsState
from api.llm_api.llm_api import LLMApi
from api.news_api.main import NewsAPI
from api.tts_api.main import TTSAPI
from usecases.state_machine import StateMachine


class TestNewsState(unittest.TestCase):
    def setUp(self):
        # Set up mocks
        self.mock_llm_api = MagicMock(spec=LLMApi)
        self.mock_news_api = MagicMock(spec=NewsAPI)
        self.mock_tts_api = MagicMock(spec=TTSAPI)
        self.mock_state_machine = MagicMock(spec=StateMachine)
        self.mock_state_machine.news_idle = MagicMock()

        # Mock API factory behavior
        self.mock_api_factory = MagicMock()
        self.mock_api_factory.create_api.side_effect = (
            lambda api_type: self.mock_news_api if api_type == "news" else self.mock_tts_api
        )
        self.mock_state_machine.api_factory = self.mock_api_factory
        self.mock_api_factory.create_api.return_value = self.mock_tts_api
        self.mock_api_factory.create_api.side_effect = lambda api_type: self.mock_news_api if api_type == "news" else self.mock_tts_api

        # Create NewsState instance
        self.news_state = NewsState(self.mock_state_machine)

    @patch.object(NewsAPI, 'get_article', return_value="Full article content")
    @patch.object(NewsAPI, 'summarize_article', return_value="Summarized content")
    @patch.object(LLMApi, 'get_response', return_value="1")  # Ensure a valid response
    def test_read_article(self, mock_llm_response, mock_summarize, mock_get_article):
        # Mock TTS listen return value
        self.mock_tts_api.listen.side_effect = ["yes", "1"]  # Simulate valid input for article selection

        # Mock headlines
        headlines = ["Headline 1", "Headline 2", "Headline 3"]

        # Call read_article
        result = self.news_state.read_article(headlines)

        # Assertions
        mock_get_article.assert_called_once_with(1)  # Ensure this is called
        mock_summarize.assert_called_once_with("Full article content")
        self.mock_tts_api.speak.assert_any_call("Summarized content")
        self.assertEqual(result, "exit")



    @patch.object(NewsState, 'read_article', return_value="exit")
    def test_on_enter(self, mock_read_article):
        # Mock headlines and behavior
        self.mock_news_api.get_headlines.return_value = ["Headline 1", "Headline 2", "Headline 3"]

        # Run on_enter method
        self.news_state.on_enter()

        # Verify TTS API announces headlines
        expected_calls = [
            call("Headline: Headline 1"),
            call("Headline: Headline 2"),
            call("Headline: Headline 3"),
            call("Wollen sie die Zusammenfassung eines Artikels hören?"),
        ]
        self.mock_tts_api.speak.assert_has_calls(expected_calls, any_order=False)

        # Verify read_article is triggered
        mock_read_article.assert_called_once()

        # Verify state machine transitions back to idle
        self.mock_state_machine.news_idle.assert_called_once()

    def test_read_article_edge_cases(self):
        # Test with empty headlines
        result_empty = self.news_state.read_article([])
        self.mock_tts_api.speak.assert_called_with(
            "Es tut mir leid, ich konnte den Artikel nicht zusammenfassen."
        )
        self.assertEqual(result_empty, "exit")

        # Test with invalid user input
        self.mock_tts_api.listen.return_value = "invalid"
        result_invalid = self.news_state.read_article(["Headline 1", "Headline 2"])
        self.mock_tts_api.speak.assert_called_with('Es tut mir leid, ich konnte den Artikel nicht zusammenfassen.')
        self.assertEqual(result_invalid, "exit")


if __name__ == "__main__":
    unittest.main()
