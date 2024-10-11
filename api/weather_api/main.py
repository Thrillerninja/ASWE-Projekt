from typing import Dict
from api.api_client import APIClient

class WeatherAPI(APIClient):
    """
    API client for accessing weather data from OpenWeatherMap.
    """

    def __init__(self, api_key: str):
        """
        Initializes the WeatherAPI client with the provided API key.

        :param api_key: OpenWeatherMap API key.
        """
        super().__init__('https://api.openweathermap.org/data/2.5')
        self.api_key = api_key

    def authenticate(self):
        """
        OpenWeatherMap uses API keys passed as query parameters.
        No additional authentication steps are required.
        """
        pass  # Authentication handled via API key in parameters

    def get_weather(self, city: str, units: str = 'metric') -> Dict:
        """
        Retrieves current weather data for the specified city.

        :param city: Name of the city (e.g., "London").
        :param units: Units of measurement ('metric', 'imperial', or 'standard').
        :return: Weather data as a dictionary.
        """
        params = {
            'q': city,
            'appid': self.api_key,
            'units': units
        }
        return self.get('weather', params=params)