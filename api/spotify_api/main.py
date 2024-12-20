from typing import Dict, Optional, List
import json
import requests
from loguru import logger
from api.spotify_api.spotify_auth import get_access_token
from api.api_client import APIClient

class SpotifyAPI(APIClient):
    """
    Spotify API client for interacting with Spotify endpoints.
    Automatically updates the token before each request.
    """

    def __init__(self, client_id, client_secret):
        """
        Initializes the Spotify API client with the base URL.
        """
        base_url = "https://api.spotify.com/v1"
        self.client_id = client_id
        self.client_secret = client_secret
        super().__init__(base_url=base_url)
        self.update_token()

    def authenticate(self) -> str:
        """
        Authenticates with the Spotify API by retrieving an access token.
        :return: Access token as a string.
        """
        return get_access_token(self.client_id, self.client_secret)

    def update_token(self):
        """
        Updates the access token and refreshes headers with the new token.
        """
        logger.info("Updating access token")
        self.access_token = self.authenticate()
        self.headers = {"Authorization": f"Bearer {self.access_token}"}

    def get_user_playlists(self) -> List[Dict]:
        """
        Retrieves the current user's playlists.
        
        :return: List of playlists as dictionaries.
        """
        logger.info("Retrieving user playlists")
        endpoint = "me/playlists"
        params = {
            "limit": 5,  # Maximum allowed by Spotify API is 50
            "offset": 0
        }
        self.update_token()
        response = super().get(endpoint, params=params)
        return response['items']  # List of playlist items
    
    def get_available_devices(self) -> List[Dict]:
        """
        Retrieves a list of available devices for playback.
        
        :return: List of devices as dictionaries.
        """
        logger.info("Retrieving available devices")
        endpoint = "me/player/devices"
        response = self.get(endpoint)
        return response['devices']  # List of devices

    def start_playback(self, playlist_id: str, device_id: Optional[str] = None) -> None:
        """
        Starts playback of a specified playlist on the user's active device.
        
        :param playlist_id: The ID of the playlist to play.
        :param device_id: Optional ID of the device to use for playback.
        """
        logger.info(f"Starting playback for playlist: {playlist_id} on device: {device_id}")
        endpoint = "me/player/play"
        data = {
            "context_uri": f"spotify:playlist:{playlist_id}",
            "position_ms": 0
        }
        
        if device_id:
            data["device_id"] = device_id
        json_data = json.dumps(data)

        self.update_token()
        try:
            response = super().put(endpoint, data=json_data)
        except requests.exceptions.HTTPError:
            logger.error(f"ERROR playing music: Device '{device_id}' is not active.")
            return
        
        if response.status_code == 204:
            logger.info("Playback started successfully!")
        else:
            try:
                response_json = response.json()
            except ValueError as e:
                logger.error(f"Error parsing response: {e}")
                response_json = None

            logger.error(f"Failed to start playback: {response_json or 'No response content'}")
            raise Exception(f"Failed to start playback: {response_json or 'No response content'}")
        
    def pause_playback(self, device_id: Optional[str] = None) -> None:
        """
        Pauses the current playback on the user's active device.
        """
        endpoint = "me/player/pause"
        
        try:
            response = super().put(endpoint, data={"device_id": device_id})
        except requests.exceptions.HTTPError:
            print(f"ERROR stopping music: Device '{device_id}' is not active.")
            return
        
        
        if response.status_code == 200 or response.status_code == 204:
            print("Playback paused successfully!")
        else:
            try:
                response_json = response.json()
            except ValueError as e:
                print(f"Error parsing response: {e}")
                response_json = None

            raise Exception(f"Failed to pause playback: {response_json or 'No response content'}")
