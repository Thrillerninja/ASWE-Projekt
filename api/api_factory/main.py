from typing import Dict
from api.api_client import APIClient
from api.news_api import NewsAPI
from api.weather_api import WeatherAPI
from api.news_api import NewsAPI
from api.weather_api import WeatherAPI
from api.finance_api import FinanceAPI
from api.spotify_api import SpotifyAPI
from api.fitbit_api import FitbitAPI

from api.calendar_api import RaplaAPI
from api.tts_api import TTSAPI
from api.vvs_api import VVSAPI
from api.vvs_api import VVSAPI

class APIFactory:
    """
    Factory class to create instances of different API clients.
    """
    _instances = {}
    _instances = {}

    def __init__(self, config: Dict):
        self.config = config
        self.toggle_elevenlabs = False

    def create_api(self, api_type: str) -> APIClient:
        """
        Creates and returns an instance of the specified API client.

        :param api_type: Type of API client to create (e.g., 'weather').
        :return: Instance of a subclass of APIClient.
        :raises ValueError: If the api_type is not supported.
        """
        if api_type not in self._instances:
            if api_type == 'weather':
                self._instances[api_type] = WeatherAPI(self.config['weather_api_key'])
            elif api_type == 'finance':
                self._instances[api_type] = FinanceAPI(self.config['finance_api_key'])
            elif api_type == 'spotify':
                self._instances[api_type] = SpotifyAPI(
                    client_id=self.config['spotify_client_id'],
                    client_secret=self.config['spotify_client_secret']
                )
            elif api_type == 'fitbit':
                self._instances[api_type] =  FitbitAPI(
                    self.config['fitbit_client_id'], 
                    self.config['fitbit_client_secret']
                )
            elif api_type == 'rapla':
                self._instances[api_type] = RaplaAPI(self.config['rapla_url'])
            elif api_type == 'tts':
                self._instances[api_type] = TTSAPI(self.config['elevenlabs_key'], self.toggle_elevenlabs)#TODO: toggle_elevenlabs aus preferences auslesen
            elif api_type == 'vvs':
                self._instances[api_type] = VVSAPI()
            elif api_type == 'news':
                self._instances[api_type] = NewsAPI()
            else:
                raise ValueError(f"API type '{api_type}' is not supported.")
        return self._instances[api_type]