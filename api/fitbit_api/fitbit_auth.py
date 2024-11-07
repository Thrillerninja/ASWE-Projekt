import json
import os
import time
import base64
import uuid
from requests_oauthlib import OAuth2Session
import requests
from urllib.parse import urlparse, parse_qs


class FitbitAuth:
    """
    Handles OAuth2 authentication for the Fitbit API.

    This class manages the process of obtaining, refreshing, and storing OAuth2 tokens 
    to access the Fitbit API. It supports both initial authorization and token renewal.
    """

    AUTHORIZATION_BASE_URL = "https://api.fitbit.com/oauth2/authorize"
    TOKEN_URL = "https://api.fitbit.com/oauth2/token"
    SCOPE = ["profile", "heartrate", "activity", "sleep", "weight", "location"]
    REDIRECT_URI = "https://127.0.0.1:8080"

    def __init__(self, client_id: str, client_secret: str):
        """
        Initializes the FitbitAuth instance and loads any previously saved tokens from file.

        :return: None
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        self.refresh_token = None
        self.expires_at = None
        self.TOKEN_FILE = os.path.join(
            os.path.dirname(__file__), "fitbit_tokens.json"
        )  
        self.load_tokens()

    def save_tokens(self, tokens):
        """
        Saves the access and refresh tokens to a JSON file.

        :param tokens: Dictionary containing 'access_token', 'refresh_token', and 'expires_at' values.
        :return: None
        """
        try:
            with open(self.TOKEN_FILE, "w") as f:
                json.dump(tokens, f, indent=4)
            print("Tokens successfully saved.")
        except IOError as e:
            print("Error saving tokens:", e)

    def load_tokens(self):
        """
        Loads tokens from a JSON file if available. Populates access_token, refresh_token,
        and expires_at attributes if successful.

        :return: None
        """
        if os.path.exists(self.TOKEN_FILE):
            try:
                with open(self.TOKEN_FILE, "r") as f:
                    tokens = json.load(f)
                    self.access_token = tokens.get("access_token")
                    self.expires_at = tokens.get("expires_at")
                    self.refresh_token = tokens.get("refresh_token")
                print("Tokens successfully loaded.")
            except (IOError, json.JSONDecodeError) as e:
                print("Error loading tokens:", e)

    def get_access_token(self):
        """
        Returns a valid access token. If the current token is expired, it is refreshed.

        :return: Valid access token as a string.
        """
        if self.expires_at and time.time() >= self.expires_at:
            print("Access token expired. Refreshing...")
            self.refresh_access_token()
        else:
            print("Access token is still valid.")
        return self.access_token

    def refresh_access_token(self):
        """
        Refreshes the access token using the refresh token.

        :raises Exception: If token refresh fails or no refresh token is available.
        :return: None
        """
        if self.refresh_token:

            auth_header = base64.b64encode(
                f"{self.client_id}:{self.client_secret}".encode()
            ).decode()

            response = requests.post(
                self.TOKEN_URL,
                headers={
                    "Authorization": f"Basic {auth_header}",
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                data={
                    "grant_type": "refresh_token",
                    "refresh_token": self.refresh_token,
                },
            )

            if response.status_code == 200:
                new_tokens = response.json()
                new_tokens["expires_at"] = time.time() + new_tokens["expires_in"]
                self.access_token = new_tokens["access_token"]
                self.expires_at = new_tokens["expires_at"]
                self.refresh_token = new_tokens["refresh_token"]
                self.save_tokens(new_tokens)
                print("Access token successfully refreshed.")
            else:
                print(f"Refresh token {self.refresh_token}")
                print("Error refreshing token:", response.json())
        else:
            print("No refresh token available. Please re-authenticate.")

    def authorize(self):
        """
        Initiates the OAuth2 authorization flow for the user.

        This method directs the user to the Fitbit authorization URL. Once authorized,
        it fetches the initial access and refresh tokens and saves them to file.

        :return: None
        """
        state = str(uuid.uuid4())
        fitbit = OAuth2Session(
            self.client_id,
            scope=self.SCOPE,
            redirect_uri=self.REDIRECT_URI,
            state=state,
        )
        authorization_url, _ = fitbit.authorization_url(
            self.AUTHORIZATION_BASE_URL, prompt="consent"
        )

        print("Please authorize the application here:", authorization_url)
        redirect_response = input("Paste the full redirect URL here: ")

        parsed_url = urlparse(redirect_response)
        code = parse_qs(parsed_url.query).get("code", [None])[0]

        if code:
            token_response = fitbit
