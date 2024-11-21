import unittest
from unittest.mock import MagicMock, patch, call
from usecases.news_state import NewsState
from api.llm_api.llm_api import LLMApi
from api.news_api.main import NewsAPI
from api.tts_api.main import TTSAPI
from usecases.state_machine import StateMachine  # Beispiel für den Import von StateMachine

class TestNewsState(unittest.TestCase):
    
    def setUp(self):
        # Mocking der API-Objekte
        self.mock_llm_api = MagicMock(spec=LLMApi)
        self.mock_news_api = MagicMock(spec=NewsAPI)
        self.mock_tts_api = MagicMock(spec=TTSAPI)

        # Mock für NewsAPI.get_headlines
        self.mock_news_api.get_headlines.return_value = [
            "Headline 1", "Headline 2", "Headline 3"
        ]

        # Mock für TTSAPI.speak
        self.mock_tts_api.speak = MagicMock()

        # Mock für die StateMachine
        self.mock_state_machine = MagicMock(spec=StateMachine)

        # Hier den api_factory Mock explizit hinzufügen
        self.mock_api_factory = MagicMock()
        self.mock_state_machine.api_factory = self.mock_api_factory
        self.mock_api_factory.create_api.return_value = self.mock_tts_api

        # Mock für die Methode news_idle
        self.mock_state_machine.news_idle = MagicMock()

        # Erstellen des NewsState Objekts mit den gemockten APIs
        self.news_state = NewsState(self.mock_state_machine)

    @patch.object(NewsState, 'read_article', return_value="exit")  # Mocking der read_article Methode
    @patch.object(NewsAPI, 'get_headlines', return_value=["Headline 1", "Headline 2", "Headline 3"])  # Mocking get_headlines
    def test_on_enter(self, mock_get_headlines, mock_read_article):
        # Simulieren des Zustandswechsels und der Ausführung von on_enter
        self.news_state.on_enter()
        
        # Überprüfen, ob die Headlines korrekt durch die TTS-API vorgelesen wurden
        expected_calls = [
            call("Headline: Headline 1"),
            call("Headline: Headline 2"),
            call("Headline: Headline 3"),
            call("Wollen sie die Zusammenfassung eines Artikels hören?")
        ]
        
        # Überprüfen, ob die speak Methode mit den richtigen Parametern in der richtigen Reihenfolge aufgerufen wurde
        self.mock_tts_api.speak.assert_has_calls(expected_calls)
        
        # Überprüfen, ob die read_article Methode aufgerufen wurde
        mock_read_article.assert_called()

        # Überprüfen, ob der Übergang in den Idle-Zustand nach dem Durchlaufen des NewsState erfolgt ist
        self.mock_state_machine.news_idle.assert_called_once()

    @patch.object(NewsAPI, 'get_article', return_value="Article content")  # Mocking get_article
    @patch.object(NewsAPI, 'summarize_article', return_value="Summary of article")  # Mocking summarize_article
    @patch.object(LLMApi, 'get_response', return_value="1")  # Mocking LLMApi.get_response
    def test_read_article(self, mock_get_response, mock_summarize_article, mock_get_article):
        # Simulieren des Aufrufs der read_article-Methode
        headlines = ["Headline 1", "Headline 2", "Headline 3"]
        
        # Führen der Methode aus, die wir testen wollen
        result = self.news_state.read_article(headlines)
        
        # Überprüfen, ob LLMApi.get_response mit der richtigen Nachricht aufgerufen wurde
        message = (
            f"This is input from a user: {self.mock_tts_api.listen.return_value}. "
            f"These are possible headlines: {headlines}. "
            f"Which headline interests the user the most? Respond with the number of the headline."
        )
        mock_get_response.assert_called_once_with(model="llama3.2:1b", message_content=message)
        
        # Überprüfen, ob die richtigen Artikelinformationen abgerufen wurden
        mock_get_article.assert_called_once_with(1)
        mock_summarize_article.assert_called_once_with("Article content")
        
        # Überprüfen, ob die TTS-API das richtige Ergebnis spricht
        self.mock_tts_api.speak.assert_any_call("Summary of article")
        
        # Sicherstellen, dass die Methode 'exit' zurückgibt
        self.assertEqual(result, "exit")
    
if __name__ == '__main__':
    unittest.main()
