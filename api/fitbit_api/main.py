import requests
from api.fitbit_api.fitbit_auth import FitbitAuth  
from api.api_client import APIClient

class FitbitAPI(APIClient):
    """
    API client for accessing data from Fitbit.
    """

    API_URL_HEART = '1/user/-/activities/heart/date/{}/1d/1min.json'
    API_URL_STEPS = '1/user/-/activities/steps/date/{}/1d/1min.json'
    API_URL_SLEEP = '1.2/user/-/sleep/date/{}.json'

    def __init__(self, client_id: str, client_secret: str):
        """
        Initializes the FitbitAPI client with the provided credentials.
        :param client_id: Fitbit API Client ID.
        :param client_secret: Fitbit API Client Secret.
        """
        self.client_id=client_id
        self.client_secret=client_secret
        self.auth = FitbitAuth(self.client_id, self.client_secret)
        base_url = "https://api.fitbit.com"
        super().__init__(base_url) 

    def authenticate(self):
        """
        Updates headers with the current access token.
        """
        access_token = self.auth.get_access_token()
        self.headers.update({'Authorization': f'Bearer {access_token}'})

    def get_heart_data(self, date: str) -> dict:
        """
        Retrieves heart rate data for a specific date.
        :param date: Date for which heart rate data is to be retrieved, in 'YYYY-MM-DD' format.
        :return: JSON response with detailed heart rate data for the specified day.
        """
        self.authenticate()  # Aktualisiert das Authorization-Header
        return self.get(self.API_URL_HEART.format(date))

    def get_steps_data(self, date: str) -> dict:
        """
        Retrieves step count data for a specific date.
        :param date: Date for which step count data is to be retrieved, in 'YYYY-MM-DD' format.
        :return: JSON response with detailed step count data for the specified day.
        """
        self.authenticate()
        return self.get(self.API_URL_STEPS.format(date))

    def get_sleep_data(self, date: str) -> dict:
        """
        Retrieves sleep data for a specific date.
        :param date: Date for which sleep data is to be retrieved, in 'YYYY-MM-DD' format.
        :return: JSON response with detailed sleep data for the specified day.
        """
        self.authenticate()
        return self.get(self.API_URL_SLEEP.format(date))