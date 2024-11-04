import requests
from fitbit_auth import FitbitAuth  

class FitbitAPI():
    """
    API client for accessing data from Fitbit.
    """

    API_URL_HEART = 'https://api.fitbit.com/1/user/-/activities/heart/date/{}/1d/1min.json'
    API_URL_STEPS = 'https://api.fitbit.com/1/user/-/activities/steps/date/{}/1d/1min.json'
    API_URL_SLEEP = 'https://api.fitbit.com/1/user/-/sleep/date/{}/json'

    def __init__(self, client_id: str, client_secret: str):
        """
        Initializes the FitbitAPI client with the provided credentials.

        :param client_id: Fitbit API Client ID.
        :param client_secret: Fitbit API Client Secret.
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.auth = FitbitAuth(client_id, client_secret) 

    def get_heart_data(self, date: str) -> dict:
        """
        Retrieves heart rate data for a specific date.

        :param date: Date for which heart rate data is to be retrieved, in 'YYYY-MM-DD' format.
        :return: JSON response with detailed heart rate data for the specified day.
        :raises HTTPError: If the request fails.
        """
        access_token = self.auth.get_access_token()
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(self.API_URL_HEART.format(date), headers=headers)
        response.raise_for_status()
        return response.json()

    def get_steps_data(self, date: str) -> dict:
        """
        Retrieves step count data for a specific date.

        :param date: Date for which step count data is to be retrieved, in 'YYYY-MM-DD' format.
        :return: JSON response with detailed step count data for the specified day.
        :raises HTTPError: If the request fails.
        """
        access_token = self.auth.get_access_token()
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(self.API_URL_STEPS.format(date), headers=headers)
        response.raise_for_status()
        return response.json()

    def get_sleep_data(self, date: str) -> dict:
        """
        Retrieves sleep data for a specific date.

        :param date: Date for which sleep data is to be retrieved, in 'YYYY-MM-DD' format.
        :return: JSON response with detailed sleep data for the specified day.
        :raises HTTPError: If the request fails.
        """
        access_token = self.auth.get_access_token()
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(self.API_URL_SLEEP.format(date), headers=headers)
        response.raise_for_status()
        return response.json()
