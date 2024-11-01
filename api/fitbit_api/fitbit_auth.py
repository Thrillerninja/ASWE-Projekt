import json
import os
import time
import base64
import uuid
from requests_oauthlib import OAuth2Session
import requests
from urllib.parse import urlparse, parse_qs


class FitbitAuth:
    CLIENT_ID = "23PQNT"
    CLIENT_SECRET = "db957a4b0cbbcedfecf8a384631dd514"
    AUTHORIZATION_BASE_URL = "https://api.fitbit.com/oauth2/authorize"
    TOKEN_URL = "https://api.fitbit.com/oauth2/token"
    SCOPE = ["profile", "heartrate", "activity", "sleep", "weight", "location"]
    REDIRECT_URI = "https://127.0.0.1:8080"

    def __init__(self):
        self.access_token = None
        self.refresh_token = None
        self.expires_at = None
        self.TOKEN_FILE = os.path.join(
            os.path.dirname(__file__), "fitbit_tokens.json"
        )  # Dynamisch den Pfad setzen
        self.load_tokens()

    def save_tokens(self, tokens):
        try:
            with open(self.TOKEN_FILE, "w") as f:
                json.dump(tokens, f, indent=4)
            print("Tokens erfolgreich gespeichert.")
        except IOError as e:
            print("Fehler beim Speichern der Tokens:", e)

    def load_tokens(self):
        if os.path.exists(self.TOKEN_FILE):
            try:
                with open(self.TOKEN_FILE, "r") as f:
                    tokens = json.load(f)
                    self.access_token = tokens.get("access_token")
                    self.expires_at = tokens.get("expires_at")
                    self.refresh_token = tokens.get("refresh_token")
                print("Tokens erfolgreich geladen.")
            except (IOError, json.JSONDecodeError) as e:
                print("Fehler beim Laden der Tokens:", e)

    def get_access_token(self):
        if self.expires_at and time.time() >= self.expires_at:
            print("Access Token abgelaufen. Erneuern...")
            self.refresh_access_token()
        else:
            print("Access Token ist noch aktuell.")
        return self.access_token

    def refresh_access_token(self):
        if self.refresh_token:

            # Erstellen des Authorization Headers
            auth_header = base64.b64encode(
                f"{self.CLIENT_ID}:{self.CLIENT_SECRET}".encode()
            ).decode()
            # Senden der Anfrage zur Token-Erneuerung
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

            # Überprüfen, ob die Token-Erneuerung erfolgreich war
            if response.status_code == 200:
                new_tokens = response.json()
                new_tokens["expires_at"] = time.time() + new_tokens["expires_in"]
                self.access_token = new_tokens["access_token"]
                self.expires_at = new_tokens["expires_at"]
                self.refresh_token = new_tokens["refresh_token"]
                self.save_tokens(new_tokens)
                print("Access Token erfolgreich erneuert.")
            else:
                print(f"Refresh token {self.refresh_token}")
                print("Fehler beim Token-Erneuern:", response.json())
        else:
            print(
                "Kein Refresh Token vorhanden. Bitte authentifizieren Sie sich erneut."
            )

    def authorize(self):
        state = str(uuid.uuid4())
        fitbit = OAuth2Session(
            self.CLIENT_ID,
            scope=self.SCOPE,
            redirect_uri=self.REDIRECT_URI,
            state=state,
        )
        authorization_url, _ = fitbit.authorization_url(
            self.AUTHORIZATION_BASE_URL, prompt="consent"
        )

        print("Bitte autorisieren Sie die Anwendung hier:", authorization_url)
        redirect_response = input("Fügen Sie die vollständige URL hier ein: ")

        parsed_url = urlparse(redirect_response)
        code = parse_qs(parsed_url.query).get("code", [None])[0]

        if code:
            token_response = fitbit.fetch_token(
                self.TOKEN_URL,
                authorization_response=redirect_response,
                client_secret=self.CLIENT_SECRET,
            )
            token_response["expires_at"] = time.time() + token_response["expires_in"]
            self.access_token = token_response["access_token"]
            self.expires_at = token_response["expires_at"]
            self.refresh_token = token_response["refresh_token"]
            self.save_tokens(token_response)
            print("Autorisiert und Tokens gespeichert.")
        else:
            print("Fehler: Keine Autorisierung erhalten.")
