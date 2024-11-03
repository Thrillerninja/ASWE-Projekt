import datetime
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
            super().__init__('https://api.openweathermap.org')
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
        return self.get('data/2.5/weather', params=params)
    
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
        response = self.get('data/2.5/forecast', params=params)
        return response
    
    def get_formated_forecast(self, city: str, units: str = 'metric') -> str:
        """
        Retrieves the formatted weather forecast for the specified city.
        
        :param city: Name of the city (e.g., "Berlin").
        :param units: Units of measurement ('metric', 'imperial', or 'standard').
        :return: Formatted weather forecast as a string.
        """
        response = self.get_forecast(city, units)
        daily_forecast = {}
        for item in response['list']:
            date = item['dt_txt'].split(' ')[0]
            if date not in daily_forecast:
                daily_forecast[date] = {
                    'temp_min': item['main']['temp_min'],
                    'temp_max': item['main']['temp_max'],
                    'description': item['weather'][0]['description']
                }
            else:
                daily_forecast[date]['temp_min'] = min(daily_forecast[date]['temp_min'], item['main']['temp_min'])
                daily_forecast[date]['temp_max'] = max(daily_forecast[date]['temp_max'], item['main']['temp_max'])
            
        formatted_forecast = []
        for date, data in daily_forecast.items():
            formatted_forecast.append(f"{data['temp_min']}°C to {data['temp_max']}°C, {data['description']}")
        
        return "Aktuelles Wetter" + formatted_forecast[0] + " Heute Mittag" + formatted_forecast[len(formatted_forecast)//2]

    def get_daily_forecast(self, city: str, date: datetime.date = datetime.datetime.today(), units: str = 'metric') -> Dict:
        """
        Calcs the daily weather forecast for the given location.

        :param city: Name of the city (e.g., "Berlin").
        :param date: Date for the forecast (defaults to today if not provided).
        :param units: Units of measurement ('metric', 'imperial', or 'standard').
        :return: Daily weather forecast as a dictionary.
        """
        
        # GEt 5day/3hr forecast
        forecast = self.get_forecast(city, units)
        # Get all forcast windows for the given date
        date_str = date.strftime('%Y-%m-%d')
        weather = None
        for item in forecast['list']:
            if item['dt_txt'].startswith(date_str):
                if not weather:
                    weather = []
                weather.append(item)
                
        if not weather:
            return {}

        # Extract relevant data
        day_min_temp = float('inf')
        day_max_temp = float('-inf')
        day_avg_temp = 0
        conditions = {}

        for datapoint in weather:
            day_min_temp = min(day_min_temp, datapoint['main']['temp_min'])
            day_max_temp = max(day_max_temp, datapoint['main']['temp_max'])
            day_avg_temp += datapoint['main']['temp']
            condition = datapoint['weather'][0]['description']
            if condition in conditions:
                conditions[condition] += 1
            else:
                conditions[condition] = 1

        day_avg_temp /= len(weather)
        avg_condition = max(conditions, key=conditions.get)

        daily_forecast_data = {
            'min_temp': day_min_temp,
            'max_temp': day_max_temp,
            'avg_temp': day_avg_temp,
            'avg_condition': avg_condition
        }
        return daily_forecast_data

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
    
    def get_city_coords(self, city: str) -> Dict:
        """
        Retrieves the coordinates of the specified city.

        :param city: Name of the city (e.g., "Berlin").
        :return: City coordinates as a dictionary.
        """
        params = {
            'q': city,
            'appid': self.api_key
        }
        response = self.get('geo/1.0/direct', params=params)
        coords = {
                'lat': response[0]['lat'],
                'lon': response[0]['lon']
            }
        return coords