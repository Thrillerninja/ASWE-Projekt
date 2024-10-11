import os
from dotenv import load_dotenv, find_dotenv

# Load environment variables from a .env file
dotenv_path = find_dotenv()
if not dotenv_path:
    raise FileNotFoundError("Could not find a .env file")
load_dotenv(dotenv_path)

def get_env_variable(var_name):
    value = os.getenv(var_name)
    if value is None:
        raise EnvironmentError(f"Required environment variable '{var_name}' is not set.")
    return value

CONFIG = {
      'weather_api_key': get_env_variable('WEATHER_API_KEY'),
#     'maps_api_key': get_env_variable('MAPS_API_KEY'),
#     'spotify_client_id': get_env_variable('SPOTIFY_CLIENT_ID'),
#     'spotify_client_secret': get_env_variable('SPOTIFY_CLIENT_SECRET'),
#     'spotify_refresh_token': get_env_variable('SPOTIFY_REFRESH_TOKEN'),
#     'news_api_key': get_env_variable('NEWS_API_KEY'),
}