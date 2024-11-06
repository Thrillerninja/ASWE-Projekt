import unittest
import os
from unittest.mock import patch, MagicMock
from api.fitbit_api import FitbitAPI

class TestFitbitAPI(unittest.TestCase):

    def setUp(self):
        """
        Initializes the test setup with mock Fitbit credentials and test date.
        Simulates environment variables for testing without actual secrets.
        """
        # Simulate environment variables
        os.environ['FITBIT_CLIENT_ID'] = 'test_client_id'
        os.environ['FITBIT_CLIENT_SECRET'] = 'test_client_secret'
        
        self.fitbit_client_id = os.getenv('FITBIT_CLIENT_ID')
        self.fitbit_client_secret = os.getenv('FITBIT_CLIENT_SECRET')
        
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
        mock_response = MagicMock()
        expected_data = {'activities-heart-intraday': {'dataset': [{'time': '09:30:00', 'value': 70}]}}
        mock_response.json.return_value = expected_data
        mock_get.return_value = mock_response

        heart_data = self.fitbit_api.get_heart_data(self.date)
        self.assertEqual(heart_data, expected_data)
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
