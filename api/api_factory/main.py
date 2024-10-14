from typing import Dict
from api.api_client import APIClient
from api.weather_api import WeatherAPI
from api.calendar_api import RaplaAPI

class APIFactory:
    """
    Factory class to create instances of different API clients.
    """

    def __init__(self, config: Dict):
        """
        Initializes the factory with configuration data.

        :param config: Dictionary containing API keys and tokens.
        """
        self.config = config

    def create_api(self, api_type: str) -> APIClient:
        """
        Creates and returns an instance of the specified API client.

        :param api_type: Type of API client to create (e.g., 'weather').
        :return: Instance of a subclass of APIClient.
        :raises ValueError: If the api_type is not supported.
        """
        if api_type == 'weather':
            return WeatherAPI(self.config['weather_api_key'])
        elif api_type == 'calendar':
            return RaplaAPI(self.config['start_year'], self.config['class_letter'], self.config['email'])
        # elif api_type == 'maps':
            # return MapsAPI(self.config['maps_api_key'])
        # elif api_type == 'spotify':
            # return SpotifyAPI(
                # client_id=self.config['spotify_client_id'],
                # client_secret=self.config['spotify_client_secret'],
                # refresh_token=self.config['spotify_refresh_token']
            # )
        # elif api_type == 'news':
            # return NewsAPI(self.config['news_api_key'])
        else:
            raise ValueError(f"API type '{api_type}' is not supported.")
