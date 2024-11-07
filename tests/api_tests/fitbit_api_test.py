import unittest
from unittest.mock import patch, MagicMock, mock_open
import time
import json
from api.fitbit_api.fitbit_auth import FitbitAuth


class TestFitbitAuth(unittest.TestCase):

    def setUp(self):
        self.client_id = "test_client_id"
        self.client_secret = "test_client_secret"
        self.fitbit_auth = FitbitAuth(self.client_id, self.client_secret)
        self.tokens = {
            "access_token": "test_access_token",
            "refresh_token": "test_refresh_token",
            "expires_at": time.time() + 3600,
        }

    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps({
        "access_token": "test_access_token",
        "refresh_token": "test_refresh_token",
        "expires_at": time.time() + 3600,
    }))
    def test_load_tokens(self, mock_file):
        self.fitbit_auth.load_tokens()
        self.assertEqual(self.fitbit_auth.access_token, "test_access_token")
        self.assertEqual(self.fitbit_auth.refresh_token, "test_refresh_token")
        self.assertTrue(self.fitbit_auth.expires_at > time.time())
        mock_file.assert_called_once_with(self.fitbit_auth.TOKEN_FILE, "r")

    @patch("builtins.open", new_callable=mock_open)
    def test_save_tokens(self, mock_file):
        self.fitbit_auth.save_tokens(self.tokens)
        mock_file.assert_called_once_with(self.fitbit_auth.TOKEN_FILE, "w")
        handle = mock_file()
        self.assertEqual(handle.write.call_count, 15)
        expected_output = json.dumps(self.tokens, indent=4) 
        written_content = "".join(call.args[0] for call in handle.write.call_args_list)
        
        self.assertEqual(written_content, expected_output)

    @patch("api.fitbit_api.fitbit_auth.requests.post")
    @patch.object(FitbitAuth, "save_tokens")  # Patch `save_tokens` in der `FitbitAuth` Klasse
    def test_refresh_access_token(self, mock_save_tokens, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "access_token": "test_access_token",
            "refresh_token": "test_refresh_token",
            "expires_in": 3600
        }
        mock_post.return_value = mock_response

        self.fitbit_auth.refresh_token = "test_refresh_token"

        # Simuliere den erfolgreichen API-Aufruf
        self.fitbit_auth.refresh_access_token()

   

        # Sicherstellen, dass die Tokens korrekt gesetzt wurden
        self.assertEqual(self.fitbit_auth.access_token, "test_access_token")
        self.assertEqual(self.fitbit_auth.refresh_token, "test_refresh_token")
        self.assertTrue(self.fitbit_auth.expires_at > time.time())

        # Überprüfen, dass der API-Aufruf durchgeführt wurde
        mock_post.assert_called_once()



    @patch("api.fitbit_api.fitbit_auth.requests.post")
    @patch("builtins.print")
    def test_refresh_access_token_failure(self, mock_print, mock_post):
        # Simuliere eine fehlgeschlagene Antwort
        mock_response = MagicMock()
        mock_response.status_code = 400  # Fehlerstatus (z. B. invalid_grant)
        mock_response.json.return_value = {"error": "invalid_grant"}  # Fehlerantwort von der API
        mock_post.return_value = mock_response

        # Angenommene refresh_token
        self.fitbit_auth.refresh_token = "mock_refresh_token"

        # Methode aufrufen
        self.fitbit_auth.refresh_access_token()

        # Überprüfe, ob die Fehlermeldung korrekt ausgegeben wurde
        mock_print.assert_any_call("Error refreshing token:", {"error": "invalid_grant"})

    # @patch("api.fitbit_api.fitbit_auth.OAuth2Session.authorization_url")
    # @patch("api.fitbit_api.fitbit_auth.input", return_value="https://127.0.0.1:8080?code=test_code")
    # @patch("api.fitbit_api.fitbit_auth.OAuth2Session.fetch_token")
    # def test_authorize(self, mock_fetch_token, mock_input, mock_authorization_url):
    #     # Setze den gemockten Authorization URL und den Token Fetch
    #     mock_authorization_url.return_value = ("https://authorization.url", "state")
        
    #     # Simuliere die Antwort von fetch_token (nach erfolgreicher Autorisierung)
    #     mock_token_response = {
    #         "access_token": "test_access_token",
    #         "refresh_token": "test_refresh_token",
    #         "expires_at": 3600,
    #     }
    #     mock_fetch_token.return_value = mock_token_response
        
    #     # Erstelle eine Instanz der Klasse
    #     fitbit_auth = FitbitAuth(client_id="test_client_id", client_secret="test_client_secret")
        
    #     # Führe die Methode authorize() aus
    #     fitbit_auth.authorize()
                
    #     # Überprüfe, ob die richtigen Tokens gesetzt wurden
    #     self.assertEqual(fitbit_auth.access_token, "test_access_token")
    #     self.assertEqual(fitbit_auth.refresh_token, "test_refresh_token")
    #     self.assertTrue(fitbit_auth.expires_at > time.time())

    @patch("time.time", return_value=time.time() - 1)  # Simulate token expired
    @patch.object(FitbitAuth, "refresh_access_token")
    def test_get_access_token_refresh_needed(self, mock_refresh, mock_time):
        self.fitbit_auth.expires_at = time.time() - 10  # Expired token
        self.fitbit_auth.get_access_token()
        mock_refresh.assert_called_once()

    @patch("time.time", return_value=time.time() + 3600)  # Simulate token not expired
    @patch.object(FitbitAuth, "refresh_access_token")
    def test_get_access_token_no_refresh_needed(self, mock_refresh, mock_time):
        self.fitbit_auth.expires_at = time.time() + 3600  # Valid token
        access_token = self.fitbit_auth.get_access_token()
        self.assertEqual(access_token, self.fitbit_auth.access_token)
        mock_refresh.assert_not_called()

