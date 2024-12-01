import requests
from abc import ABC, abstractmethod
from typing import Dict, Optional

class APIClient(ABC):
    """
    Abstract base class for API clients to handle common operations.
    """

    def __init__(self, base_url: str, headers: Optional[Dict[str, str]] = None):
        """
        Initializes the API client with a base URL and optional headers.

        :param base_url: The base URL for the API.
        :param headers: Optional HTTP headers to include in requests.
        """
        self.base_url = base_url
        self.headers = headers or {}

    @abstractmethod
    def authenticate(self):
        """
        Handle authentication for the API client.
        Must be implemented by subclasses.
        """
        pass

    def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """
        Sends a GET request to the specified endpoint.

        :param endpoint: API endpoint (relative to base_url).
        :param params: Query parameters for the GET request.
        :return: JSON response as a dictionary.
        """
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

    def post(self, endpoint: str, data: Optional[Dict] = None, json: Optional[Dict] = None) -> Dict:
        """
        Sends a POST request to the specified endpoint.

        :param endpoint: API endpoint (relative to base_url).
        :param data: Form data to include in the POST request.
        :param json: JSON data to include in the POST request.
        :return: JSON response as a dictionary.
        """
        url = f"{self.base_url}/{endpoint}"
        response = requests.post(url, headers=self.headers, data=data, json=json)
        response.raise_for_status()
        return response.json()

    def put(self, endpoint: str, data: Optional[Dict] = None) -> Dict:
        """
        Sends a PUT request to the specified endpoint.

        :param endpoint: API endpoint (relative to base_url).
        :param data: Data to include in the PUT request.
        :return: JSON response as a dictionary.
        """
        url = f"{self.base_url}/{endpoint}"
        response = requests.put(url, headers=self.headers, data=data)
        response.raise_for_status()

        try:
            return response.json()
        except ValueError:
            return response

    def delete(self, endpoint: str) -> Dict:
        """
        Sends a DELETE request to the specified endpoint.

        :param endpoint: API endpoint (relative to base_url).
        :return: JSON response as a dictionary.
        """
        url = f"{self.base_url}/{endpoint}"
        response = requests.delete(url, headers=self.headers)
        response.raise_for_status()
        return response.json()