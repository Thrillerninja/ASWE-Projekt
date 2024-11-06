import unittest
from unittest.mock import patch, MagicMock
from api.fitbit_api import FitbitAPI

class TestFitbitAPI(unittest.TestCase):

    def setUp(self):
        """
        Initializes the test setup with mock Fitbit credentials and test date.
        """
        self.fitbit_client_id = "test_client_id"  # Mock client ID
        self.fitbit_client_secret = "test_client_secret"  # Mock client secret

        # Instantiate the FitbitAPI client (the authentication will be mocked)
        self.fitbit_api = FitbitAPI(self.fitbit_client_id, self.fitbit_client_secret)
        self.date = '2024-10-30'  # Test date for the API calls

    @patch('api.fitbit_api.fitbit_auth.FitbitAuth.get_access_token', return_value='test_access_token')
    @patch('requests.get')
    def test_get_heart_data(self, mock_get, mock_auth):
        """
        Tests the get_heart_data method of the FitbitAPI client.
        Mocks the HTTP request to return fake heart rate data.
        """
        mock_response = MagicMock()  # Create a mock response object
        expected_data = {'activities-heart-intraday': {'dataset': [{'time': '09:30:00', 'value': 70}]}}
        mock_response.json.return_value = expected_data  # Return the expected data when json() is called
        mock_get.return_value = mock_response  # Return the mock response when requests.get is called

        # Call the method and assert the returned data matches the expected result
        heart_data = self.fitbit_api.get_heart_data(self.date)
        self.assertEqual(heart_data, expected_data)
        # Assert that requests.get was called with the correct URL and authorization header
        mock_get.assert_called_once_with(
            f'https://api.fitbit.com/1/user/-/activities/heart/date/{self.date}/1d/1min.json',
            headers={'Authorization': 'Bearer test_access_token'}
        )

    @patch('api.fitbit_api.fitbit_auth.FitbitAuth.get_access_token', return_value='test_access_token')
    @patch('requests.get')
    def test_get_steps_data(self, mock_get, mock_auth):
        """
        Tests the get_steps_data method of the FitbitAPI client.
        Mocks the HTTP request to return fake step count data.
        """
        mock_response = MagicMock()
        expected_data = {'activities-steps-intraday': {'dataset': [{'time': '09:30:00', 'value': 100}]}}
        mock_response.json.return_value = expected_data
        mock_get.return_value = mock_response

        steps_data = self.fitbit_api.get_steps_data(self.date)
        self.assertEqual(steps_data, expected_data)
        mock_get.assert_called_once_with(
            f'https://api.fitbit.com/1/user/-/activities/steps/date/{self.date}/1d/1min.json',
            headers={'Authorization': 'Bearer test_access_token'}
        )

    @patch('api.fitbit_api.fitbit_auth.FitbitAuth.get_access_token', return_value='test_access_token')
    @patch('requests.get')
    def test_get_sleep_data(self, mock_get, mock_auth):
        """
        Tests the get_sleep_data method of the FitbitAPI client.
        Mocks the HTTP request to return fake sleep data.
        """
        mock_response = MagicMock()
        expected_data = {'sleep': [{'dateOfSleep': '2021-01-01', 'minutesAsleep': 400}]}
        mock_response.json.return_value = expected_data
        mock_get.return_value = mock_response

        sleep_data = self.fitbit_api.get_sleep_data(self.date)
        self.assertEqual(sleep_data, expected_data)
        mock_get.assert_called_once_with(
            f'https://api.fitbit.com/1/user/-/sleep/date/{self.date}/json',
            headers={'Authorization': 'Bearer test_access_token'}
        )

if __name__ == '__main__':
    unittest.main()
