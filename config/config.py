import os
from dotenv import load_dotenv, find_dotenv

# Load environment variables from a .env file if it exists
dotenv_path = find_dotenv()
if dotenv_path:
    load_dotenv(dotenv_path)

def get_env_variable(var_name):
    value = os.getenv(var_name)
    if value is None:
        raise EnvironmentError(f"Required environment variable '{var_name}' is not set.")
    return value

CONFIG = {
    'weather_api_key': get_env_variable('WEATHER_API_KEY'),
    'weather_api_key': get_env_variable('WEATHER_API_KEY'),
    'finance_api_key': get_env_variable('FINANCE_API_KEY'),
    'rapla_url': "https://rapla.dhbw.de/rapla/internal_calendar?user=doelker%40verwaltung.ba-stuttgart.de&file=22A&day=30&month=9&year=2024&pages=20"
    'spotify_client_id': get_env_variable('SPOTIFY_CLIENT_ID'),
    'spotify_client_secret': get_env_variable('SPOTIFY_CLIENT_SECRET'),
}