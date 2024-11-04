import unittest
from unittest.mock import patch, MagicMock
from api.fitbit_api import FitbitAPI

class TestFitbitAPI(unittest.TestCase):

    def setUp(self):
        self.fitbit_client_id = "test_client_id"
        self.fitbit_client_secret = "test_client_secret"

        self.fitbit_api = FitbitAPI(self.fitbit_client_id, self.fitbit_client_secret)
        self.date = '2024-10-30'

    @patch('fitbit_auth.FitbitAuth.get_access_token', return_value='test_access_token')
    @patch('requests.get')
    def test_get_heart_data(self, mock_get, mock_auth):
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

    @patch('fitbit_auth.FitbitAuth.get_access_token', return_value='test_access_token')
    @patch('requests.get')
    def test_get_steps_data(self, mock_get, mock_auth):
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

    @patch('fitbit_auth.FitbitAuth.get_access_token', return_value='test_access_token')
    @patch('requests.get')
    def test_get_sleep_data(self, mock_get, mock_auth):
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