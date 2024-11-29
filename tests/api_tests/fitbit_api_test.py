import unittest
from unittest.mock import patch, MagicMock, mock_open
import time
import json
from api.fitbit_api.fitbit_auth import FitbitAuth
from api.fitbit_api.main import FitbitAPI


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

        self.fitbit_auth.refresh_token = "mock_refresh_token"
        self.fitbit_auth.refresh_access_token()
        mock_print.assert_any_call("Error refreshing token:", {"error": "invalid_grant"})

    @patch("api.fitbit_api.fitbit_auth.FitbitAuth.save_tokens")  # 3. Mock für save_tokens
    @patch("api.fitbit_api.fitbit_auth.OAuth2Session")           # 2. Mock für OAuth2Session
    @patch("builtins.input", return_value="https://redirect-url.com/?code=test_code")  # 1. Mock für Benutzerinput
    def test_authorize(self, mock_input, mock_oauth2session, mock_save_tokens):
        # Setup
        fitbit_auth = FitbitAuth(client_id="your_client_id", client_secret="your_client_secret")
        
        # Mock die OAuth2Session-Instanz
        mock_fitbit = MagicMock()
        mock_fitbit.authorization_url.return_value = ("https://auth-url.com", None)
        mock_fitbit.fetch_token.return_value = {"access_token": "test_access_token", "refresh_token": "test_refresh_token"}
        mock_oauth2session.return_value = mock_fitbit
        
        fitbit_auth.authorize()
        
        mock_fitbit.authorization_url.assert_called_once_with(
            fitbit_auth.AUTHORIZATION_BASE_URL, prompt="consent"
        )        
        mock_fitbit.fetch_token.assert_called_once_with(
            fitbit_auth.TOKEN_URL,
            client_secret="your_client_secret",
            authorization_response="https://redirect-url.com/?code=test_code"
        )
        
        mock_save_tokens.assert_called_once_with({"access_token": "test_access_token", "refresh_token": "test_refresh_token"})

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

class TestFitbitAPI(unittest.TestCase):
    def setUp(self):
        self.client_id = "test_client_id"
        self.client_secret = "test_client_secret"
        self.date = "2023-11-08"
        self.fitbit_api = FitbitAPI(self.client_id, self.client_secret)

    @patch("api.fitbit_api.fitbit_auth.FitbitAuth.get_access_token")
    def test_authenticate(self, mock_get_access_token):
        mock_access_token = "mock_access_token"
        mock_get_access_token.return_value = mock_access_token

        self.fitbit_api.authenticate()

        # Check that headers have been updated with the correct Authorization token
        self.assertIn("Authorization", self.fitbit_api.headers)
        self.assertEqual(self.fitbit_api.headers["Authorization"], f"Bearer {mock_access_token}")
        mock_get_access_token.assert_called_once()

    @patch.object(FitbitAPI, "get")
    @patch.object(FitbitAPI, "authenticate")
    def test_get_heart_data(self, mock_authenticate, mock_get):
        mock_get.return_value = {"activities-heart": [{"dateTime": self.date, "value": "70"}]}
        result = self.fitbit_api.get_heart_data(self.date)
        self.assertEqual(result, {"activities-heart": [{"dateTime": self.date, "value": "70"}]})
        mock_authenticate.assert_called_once()
        mock_get.assert_called_once_with(f"1/user/-/activities/heart/date/{self.date}/1d/1min.json")

    @patch.object(FitbitAPI, "get")
    @patch.object(FitbitAPI, "authenticate")
    def test_get_steps_data(self, mock_authenticate, mock_get):
        mock_get.return_value = {"activities-steps": [{"dateTime": self.date, "value": "5000"}]}
        result = self.fitbit_api.get_steps_data(self.date)
        self.assertEqual(result, {"activities-steps": [{"dateTime": self.date, "value": "5000"}]})
        mock_authenticate.assert_called_once()
        mock_get.assert_called_once_with(f"1/user/-/activities/steps/date/{self.date}/1d/1min.json")

    @patch.object(FitbitAPI, "get")
    @patch.object(FitbitAPI, "authenticate")
    def test_get_sleep_data(self, mock_authenticate, mock_get):
        mock_get.return_value = {"sleep": [{"dateOfSleep": self.date, "minutesAsleep": 480}]}
        result = self.fitbit_api.get_sleep_data(self.date)
        self.assertEqual(result, {"sleep": [{"dateOfSleep": self.date, "minutesAsleep": 480}]})
        mock_authenticate.assert_called_once()
        mock_get.assert_called_once_with(f"1.2/user/-/sleep/date/{self.date}.json")