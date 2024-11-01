import requests
from fitbit_auth import FitbitAuth  # Importiere die Authentifizierungsklasse

class FitbitAPI:
    """
    API client for accessing data from Fitbit.
    """

    API_URL_HEART = 'https://api.fitbit.com/1/user/-/activities/heart/date/{}/1d/1min.json'
    API_URL_STEPS = 'https://api.fitbit.com/1/user/-/activities/steps/date/{}/1d/1min.json'
    API_URL_SLEEP = 'https://api.fitbit.com/1/user/-/sleep/date/{}/json'

    def __init__(self):
        self.auth = FitbitAuth()  

    def get_heart_data(self, date: str) -> dict:
        access_token = self.auth.get_access_token()
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(self.API_URL_HEART.format(date), headers=headers)
        response.raise_for_status()
        return response.json()

    def get_steps_data(self, date: str) -> dict:
        access_token = self.auth.get_access_token()
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(self.API_URL_STEPS.format(date), headers=headers)
        response.raise_for_status()
        return response.json()

    def get_sleep_data(self, date: str) -> dict:
        access_token = self.auth.get_access_token()
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(self.API_URL_SLEEP.format(date), headers=headers)
        response.raise_for_status()
        return response.json()
