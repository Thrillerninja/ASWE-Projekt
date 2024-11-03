import json
import time
import requests
from urllib.parse import urlencode
import base64
import os

REDIRECT_URI = 'https://example.com/callback/'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
TOKEN_FILE = os.path.join(os.path.dirname(__file__), 'spotify_token.json')

def generate_auth_url(client_id):
    """
    Generates the Spotify authorization URL for user authentication.
    Instructs the user to open the URL and copy the authorization code.
    """
    params = {
        'client_id': client_id,
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'scope': 'playlist-read-private user-modify-playback-state user-read-playback-state'
    }
    auth_url = f'https://accounts.spotify.com/authorize?{urlencode(params)}'
    print("Open the following link in your browser and copy the 'code' parameter:")
    print(auth_url)

def get_initial_token(auth_code, client_id, client_secret):
    """
    Retrieves the initial access token using the authorization code.
    Saves the token to a local file for future use.

    :param auth_code: The authorization code received from Spotify after user authentication.
    """
    # Base64-encoded Client ID and Secret
    auth_str = f"{client_id}:{client_secret}"
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()

    headers = {
        'Authorization': f'Basic {b64_auth_str}'
    }
    data = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': REDIRECT_URI,
    }
    
    response = requests.post(TOKEN_URL, headers=headers, data=data)
    
    if response.status_code == 200:
        response_data = response.json()
        save_token(response_data)
        print("Token successfully retrieved and saved.")
    else:
        print("Error retrieving the token:", response.status_code)
        print(response.json())

def refresh_token(client_id, client_secret):
    """
    Refreshes the access token using the stored refresh token.
    Updates the local token file with the new access token.
    """
    with open(TOKEN_FILE, 'r') as f:
        token_data = json.load(f)

    headers = {
        'Authorization': 'Basic ' + (client_id + ':' + client_secret).encode('ascii').decode('latin1')
    }
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': token_data['refresh_token']
    }
    response = requests.post(TOKEN_URL, headers=headers, data=data)
    response_data = response.json()

    save_token(response_data)

def save_token(data):
    """
    Saves the access and refresh tokens to a file with their expiration time.

    :param data: The token data returned by the Spotify API.
    """
    data['expires_at'] = time.time() + data['expires_in']
    with open(TOKEN_FILE, 'w') as f:
        json.dump(data, f)

def get_access_token():
    """
    Retrieves the current access token, refreshing it if it has expired.
    Raises an error if the token file does not exist.

    :return: The current access token as a string.
    """
    try:
        with open(TOKEN_FILE, 'r') as f:
            token_data = json.load(f)

        if token_data['expires_at'] < time.time():
            refresh_token()
            with open(TOKEN_FILE, 'r') as f:
                token_data = json.load(f)

        return token_data['access_token']
    except FileNotFoundError:
        print("No token found. Please run 'generate_auth_url()' and 'get_initial_token(code)' first.")
