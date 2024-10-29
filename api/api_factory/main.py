from typing import Dict
from api.api_client import APIClient
from api.weather_api.main import WeatherAPI
from api.finance_api import FinanceAPI
from api.calendar_api import RaplaAPI
from api.tts_api import TTSAPI

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
        elif api_type == 'finance':
            return FinanceAPI(self.config['finance_api_key'])
        elif api_type == 'rapla':
            return RaplaAPI(self.config['rapla_url'])
        elif api_type == 'tts':
            return TTSAPI()
        else:
            raise ValueError(f"API type '{api_type}' is not supported.")
