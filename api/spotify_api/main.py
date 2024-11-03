from typing import Dict, Optional, List
import json
from api.spotify_api.spotify_auth import get_access_token
from api.api_client import APIClient

class SpotifyAPI(APIClient):
    """
    Spotify API client for interacting with Spotify endpoints.
    Automatically updates the token before each request.
    """

    def __init__(self):
        """
        Initializes the Spotify API client with the base URL.
        """
        base_url = "https://api.spotify.com/v1"
        super().__init__(base_url=base_url)
        self.update_token()

    def authenticate(self) -> str:
        """
        Authenticates with the Spotify API by retrieving an access token.
        :return: Access token as a string.
        """
        return get_access_token()

    def update_token(self):
        """
        Updates the access token and refreshes headers with the new token.
        """
        self.access_token = self.authenticate()
        self.headers = {"Authorization": f"Bearer {self.access_token}"}

    def get_user_playlists(self) -> List[Dict]:
        """
        Retrieves the current user's playlists.
        
        :return: List of playlists as dictionaries.
        """
        endpoint = "me/playlists"
        params = {
            "limit": 10,  # Maximum allowed by Spotify API is 50
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
        endpoint = "me/player/devices"
        response = self.get(endpoint)
        return response['devices']  # List of devices

    
    def start_playback(self, playlist_id: str, device_id: Optional[str] = None) -> None:
        """
        Starts playback of a specified playlist on the user's active device.
        
        :param playlist_id: The ID of the playlist to play.
        :param device_id: Optional ID of the device to use for playback.
        """
        endpoint = "me/player/play"
        data = {
            "context_uri": f"spotify:playlist:{playlist_id}",
            "position_ms": 0
        }
        
        if device_id:
            data["device_id"] = device_id
        json_data = json.dumps(data)

        self.update_token()
        
        response = super().put(endpoint, data=json_data)
        
        if response.status_code == 204:
            print("Playback started successfully!")
        else:
            try:
                response_json = response.json()
            except ValueError as e:
                print(f"Error parsing response: {e}")
                response_json = None

            raise Exception(f"Failed to start playback: {response_json or 'No response content'}")


spotify_api = SpotifyAPI()
playlists = spotify_api.get_user_playlists()
for playlist in playlists:
    print(f"Name: {playlist['name']}")

playlist_id = playlists[0]['id']
spotify_api.start_playback(playlist_id)

#TODO Start playbackwhile music is not already running
#TODO Write tests