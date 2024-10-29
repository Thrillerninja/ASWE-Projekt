from typing import Dict
from api.api_client import APIClient

class WeatherAPI(APIClient):
    """
    API client for accessing weather data from OpenWeatherMap.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(WeatherAPI, cls).__new__(cls)
        return cls._instance

    def __init__(self, api_key: str):
        """
        Initializes the WeatherAPI client with the provided API key.

        :param api_key: OpenWeatherMap API key.
        """
        if not hasattr(self, 'initialized'):  # Ensure __init__ is only called once
            super().__init__('https://api.openweathermap.org/data/2.5')
            self.api_key = api_key
            self.initialized = True

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
            'units': units,
            'appid': self.api_key
        }
        return self.get('weather', params=params)
    
    def get_forecast(self, city: str, units: str = 'metric') -> Dict:
        """
        Retrieves weather forecast data for the specified city.

        :param city: Name of the city (e.g., "Berlin").
        :param units: Units of measurement ('metric', 'imperial', or 'standard').
        :return: Weather forecast as a string.
        """
        params = {
            'q': city,
            'appid': self.api_key,
            'units': units
        }
        response = self.get('forecast', params=params)
        forecast = self.format_forecast(response)
        return forecast
    
    def format_forecast(self, forecast: Dict) -> str:
        """
        Formats the weather forecast data into a human-readable string.

        :param forecast: Weather forecast data as a dictionary.
        :return: Formatted weather forecast as a string.
        """
        city = forecast['city']['name']
        country = forecast['city']['country']
        lines = [f"Forecast for {city}, {country}:"]
        for item in forecast['list']:
            date = item['dt_txt']
            temp = item['main']['temp']
            desc = item['weather'][0]['description']
            line = f"{date}: {temp}°C, {desc}"
            lines.append(line)
        return '\n'.join(lines)