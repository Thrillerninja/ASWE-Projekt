import unittest
from unittest.mock import patch, MagicMock, ANY, mock_open
import json
import time
import requests
from api.api_client import APIClient
from api.spotify_api.main import SpotifyAPI
from api.spotify_api.spotify_auth import generate_auth_url, get_initial_token, refresh_token, save_token, get_access_token, TOKEN_FILE
from api.api_factory import APIFactory
from config.config import CONFIG

class TestSpotifyAPI(unittest.TestCase):

    def setUp(self):
        factory = APIFactory(CONFIG)
        sp = factory.create_api('spotify')
        
        self.client_id = "test_client_id"
        self.client_secret = "test_client_secret"
        
        # Mock the token file handling
        self.mock_token_data = {
            'access_token': 'test_access_token',
            'refresh_token': 'test_refresh_token',
            'expires_in': 3600,
            'expires_at': time.time() + 3600
        }
        self.mock_open = mock_open(read_data=json.dumps(self.mock_token_data))
        with patch('builtins.open', self.mock_open):
            self.spotify_api = SpotifyAPI(self.client_id, self.client_secret)

    @patch('api.spotify_api.spotify_auth.get_access_token')
    def test_authenticate(self, mock_get_access_token):
        mock_get_access_token.return_value = "test_access_token"
        
        token = self.spotify_api.authenticate()
        
        mock_get_access_token.assert_called_once_with(self.client_id, self.client_secret)
        self.assertEqual(token, "test_access_token")

    @patch('api.spotify_api.spotify_auth.get_access_token')
    def test_update_token(self, mock_get_access_token):
        mock_get_access_token.return_value = "test_access_token"
        
        self.spotify_api.update_token()
        
        self.assertEqual(self.spotify_api.access_token, "test_access_token")
        self.assertEqual(self.spotify_api.headers, {"Authorization": "Bearer test_access_token"})

    @patch.object(APIClient, 'get')
    @patch.object(SpotifyAPI, 'update_token')
    def test_get_user_playlists(self, mock_update_token, mock_get):
        mock_get.return_value = {"items": [{"id": "playlist1"}, {"id": "playlist2"}]}
        
        playlists = self.spotify_api.get_user_playlists()
        
        mock_update_token.assert_called_once()
        mock_get.assert_called_once_with("me/playlists", params={"limit": 5, "offset": 0})
        self.assertEqual(playlists, [{"id": "playlist1"}, {"id": "playlist2"}])

    @patch.object(APIClient, 'get')
    def test_get_available_devices(self, mock_get):
        mock_get.return_value = {"devices": [{"id": "device1"}, {"id": "device2"}]}
        
        devices = self.spotify_api.get_available_devices()
        
        mock_get.assert_called_once_with("me/player/devices")
        self.assertEqual(devices, [{"id": "device1"}, {"id": "device2"}])

    @patch.object(APIClient, 'put')
    @patch.object(SpotifyAPI, 'update_token')
    @patch('loguru.logger.info')
    def test_start_playback_successful(self, mock_logger_info, mock_update_token, mock_put):
        mock_put.return_value.status_code = 204
        
        self.spotify_api.start_playback("test_playlist_id", "test_device_id")
        
        mock_update_token.assert_called_once()
        mock_put.assert_called_once_with(
            "me/player/play",
            data=json.dumps({"context_uri": "spotify:playlist:test_playlist_id", "position_ms": 0, "device_id": "test_device_id"})
        )
        mock_logger_info.assert_any_call("Playback started successfully!")

    @patch.object(APIClient, 'put')
    @patch.object(SpotifyAPI, 'update_token')
    @patch('loguru.logger.error')
    def test_start_playback_error(self, mock_logger_error, mock_update_token, mock_put):
        mock_put.side_effect = requests.exceptions.HTTPError
        
        self.spotify_api.start_playback("test_playlist_id", "test_device_id")
        
        mock_update_token.assert_called_once()
        mock_put.assert_called_once()
        mock_logger_error.assert_called_once_with("ERROR playing music: Device 'test_device_id' is not active.")

    @patch.object(APIClient, 'put')
    @patch.object(SpotifyAPI, 'update_token')
    @patch('loguru.logger.error')
    def test_start_playback_failed_response(self, mock_logger_error, mock_update_token, mock_put):
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"error": "Something went wrong"}
        mock_put.return_value = mock_response

        with self.assertRaises(Exception) as context:
            self.spotify_api.start_playback("test_playlist_id", "test_device_id")

        self.assertEqual(str(context.exception), "Failed to start playback: {'error': 'Something went wrong'}")
        mock_logger_error.assert_called_once_with("Failed to start playback: {'error': 'Something went wrong'}")

    @patch.object(APIClient, 'put')
    @patch.object(SpotifyAPI, 'update_token')
    @patch('loguru.logger.error')
    def test_start_playback_failed_response_no_json(self, mock_logger_error, mock_update_token, mock_put):
        # Mock a failed response without JSON content
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.side_effect = ValueError("No JSON content")
        mock_put.return_value = mock_response

        with self.assertRaises(Exception) as context:
            self.spotify_api.start_playback("test_playlist_id", "test_device_id")

        self.assertEqual(str(context.exception), "Failed to start playback: No response content")
        mock_logger_error.assert_any_call("Error parsing response: No JSON content")
        mock_logger_error.assert_any_call("Failed to start playback: No response content")

class TestSpotifyAuth(unittest.TestCase):

    def setUp(self):
        factory = APIFactory(CONFIG)
        sp = factory.create_api('spotify')

    @patch('builtins.print')
    def test_generate_auth_url(self, mock_print):
        client_id = 'test_client_id'
        
        generate_auth_url(client_id)

        expected_url = f'https://accounts.spotify.com/authorize?client_id={client_id}&response_type=code&redirect_uri=https%3A%2F%2Fexample.com%2Fcallback%2F&scope=playlist-read-private+user-modify-playback-state+user-read-playback-state'
        mock_print.assert_any_call(f"Open the following link in your browser and copy the 'code' parameter:")
        mock_print.assert_any_call(expected_url)

    @patch('requests.post')
    @patch('api.spotify_api.spotify_auth.save_token')
    def test_get_initial_token_success(self, mock_save_token, mock_post):
        auth_code = 'auth_code_example'
        client_id = 'test_client_id'
        client_secret = 'test_client_secret'
        
        # Mock response from the token URL
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'access_token': 'new_access_token',
            'refresh_token': 'new_refresh_token',
            'expires_in': 3600
        }
        mock_post.return_value = mock_response

        # Call the function
        get_initial_token(auth_code, client_id, client_secret)

        # Verify the POST request was made correctly
        mock_post.assert_called_once_with(
            'https://accounts.spotify.com/api/token',
            headers={
                'Authorization': 'Basic dGVzdF9jbGllbnRfaWQ6dGVzdF9jbGllbnRfc2VjcmV0'
            },
            data={
                'grant_type': 'authorization_code',
                'code': auth_code,
                'redirect_uri': 'https://example.com/callback/'
            }
        )

        # Verify that the token was saved correctly
        mock_save_token.assert_called_once_with({
            'access_token': 'new_access_token',
            'refresh_token': 'new_refresh_token',
            'expires_in': 3600
        })

    @patch('requests.post')
    @patch('builtins.print')
    def test_get_initial_token_failure(self, mock_print, mock_post):
        auth_code = 'auth_code_example'
        client_id = 'test_client_id'
        client_secret = 'test_client_secret'

        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {'error': 'invalid_grant'}
        mock_post.return_value = mock_response


        get_initial_token(auth_code, client_id, client_secret)

        mock_post.assert_called_once_with(
            'https://accounts.spotify.com/api/token',
            headers={
                'Authorization': 'Basic dGVzdF9jbGllbnRfaWQ6dGVzdF9jbGllbnRfc2VjcmV0'
            },
            data={
                'grant_type': 'authorization_code',
                'code': auth_code,
                'redirect_uri': 'https://example.com/callback/'
            }
        )

        mock_print.assert_any_call("Error retrieving the token:", 400)
        mock_print.assert_any_call({'error': 'invalid_grant'})

    @patch('requests.post')
    @patch('api.spotify_api.spotify_auth.save_token')
    @patch('builtins.open', new_callable=MagicMock)
    @patch('json.load', return_value={'refresh_token': 'old_refresh_token'})
    def test_refresh_token_success(self, mock_json_load, mock_open, mock_save_token, mock_post):
        client_id = 'test_client_id'
        client_secret = 'test_client_secret'
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'access_token': 'new_access_token',
            'refresh_token': 'new_refresh_token',
            'expires_in': 3600
        }
        mock_post.return_value = mock_response

        refresh_token(client_id, client_secret)
        
        mock_post.assert_called_once_with(
            'https://accounts.spotify.com/api/token',
            headers={
                'Authorization': 'Basic dGVzdF9jbGllbnRfaWQ6dGVzdF9jbGllbnRfc2VjcmV0',
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            data={
                'grant_type': 'refresh_token',
                'refresh_token': 'old_refresh_token'
            }
        )

        mock_save_token.assert_called_once_with({
            'refresh_token': 'new_refresh_token',
            'access_token': 'new_access_token',
            'expires_in': 3600,
            'expires_at': ANY
        })

        expected_expires_at = time.time() + 3600
        actual_expires_at = mock_save_token.call_args[0][0]['expires_at']
        tolerance = 0.5  # in seconds
        self.assertTrue(abs(actual_expires_at - expected_expires_at) < tolerance)

        mock_open.assert_called_once_with(TOKEN_FILE, 'r')

    @patch('requests.post')
    @patch('builtins.print')
    @patch('builtins.open')
    @patch('json.load')
    def test_refresh_token_failure(self, mock_json_load, mock_open, mock_print, mock_post):
        client_id = 'test_client_id'
        client_secret = 'test_client_secret'

        mock_token_data = {'refresh_token': 'old_refresh_token'}
        mock_json_load.return_value = mock_token_data

        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = "Bad Request"
        mock_post.return_value = mock_response

        mock_open.return_value.__enter__.return_value = MagicMock()

        with self.assertRaises(ConnectionRefusedError):
            refresh_token(client_id, client_secret)

        mock_print.assert_called_with('Failed to retrieve token: 400 - Bad Request')

        mock_post.assert_called_once_with(
            'https://accounts.spotify.com/api/token',
            headers={
                'Authorization': 'Basic dGVzdF9jbGllbnRfaWQ6dGVzdF9jbGllbnRfc2VjcmV0',
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            data={
                'grant_type': 'refresh_token',
                'refresh_token': 'old_refresh_token'
            }
        )

    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    @patch('json.dump')
    def test_save_token(self, mock_json_dump, mock_file):
        token_data = {
            'access_token': 'access_token_value',
            'refresh_token': 'refresh_token_value',
            'expires_in': 3600,
            'expires_at': time.time() + 3600
        }

        save_token(token_data)

        mock_file.assert_called_once_with(TOKEN_FILE, 'w')

        mock_json_dump.assert_called_once_with(token_data, mock_file())

    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    @patch('api.spotify_api.spotify_auth.refresh_token')
    def test_get_access_token_success(self, mock_refresh_token, mock_open):
        token_data = {
            'access_token': 'access_token_value',
            'refresh_token': 'refresh_token_value',
            'expires_in': 3600,
            'expires_at': time.time() + 3600
        }

        mock_open.return_value.__enter__.return_value = MagicMock()
        mock_open.return_value.__enter__.return_value.read.return_value = json.dumps(token_data)

        access_token = get_access_token('client_id', 'client_secret')

        self.assertEqual(access_token, 'access_token_value')

        mock_refresh_token.assert_not_called()

    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    @patch('api.spotify_api.spotify_auth.refresh_token')
    def test_get_access_token_expired(self, mock_refresh_token, mock_open):
        token_data = {
            'access_token': 'access_token_value',
            'refresh_token': 'refresh_token_value',
            'expires_in': 3600,
            'expires_at': time.time() - 1  # Token is expired
        }

        mock_open.return_value.__enter__.return_value = MagicMock()
        mock_open.return_value.__enter__.return_value.read.return_value = json.dumps(token_data)

        access_token = get_access_token('client_id', 'client_secret')

        mock_refresh_token.assert_called_once_with('client_id', 'client_secret')

        self.assertEqual(access_token, 'access_token_value')

    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    @patch('api.spotify_api.spotify_auth.TOKEN_FILE', new='unavailable.json')
    @patch('builtins.print')
    def test_get_access_token_file_not_found(self, mock_print, mock_open):
        mock_open.side_effect = FileNotFoundError

        get_access_token('client_id', 'client_secret')

        mock_print.assert_called_once_with(
            "No token found. Please run 'generate_auth_url()' and 'get_initial_token(code)' first."
        )

    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_get_access_token_refresh_error(self, mock_open):
        token_data = {
            'access_token': 'access_token_value',
            'refresh_token': 'refresh_token_value',
            'expires_in': 3600,
            'expires_at': time.time() - 1  # Token is expired
        }

        mock_open.return_value.__enter__.return_value = MagicMock()
        mock_open.return_value.__enter__.return_value.read.return_value = json.dumps(token_data)

        with patch('api.spotify_api.spotify_auth.refresh_token', side_effect=Exception('Failed to refresh token')):
            with self.assertRaises(Exception):
                get_access_token('client_id', 'client_secret')