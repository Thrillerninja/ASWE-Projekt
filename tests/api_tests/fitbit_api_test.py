import unittest
from unittest.mock import patch, MagicMock
from api.fitbit_api import FitbitAPI

class TestFitbitAPI(unittest.TestCase):

    def setUp(self):
        self.fitbit_api = FitbitAPI()
        self.date = '2024-10-01'

    @patch('requests.get')
    def test_get_heart_data(self, mock_get):
        mock_response = MagicMock()
        expected_data = {'activities-heart': [{'dateTime': self.date, 'value': {'restingHeartRate': 60}}]}
        mock_response.json.return_value = expected_data
        mock_get.return_value = mock_response

        heart_data = self.fitbit_api.get_heart_data(self.date)
        self.assertEqual(heart_data, expected_data)
        mock_get.assert_called_once_with(
            self.fitbit_api.API_URL_HEART.format(self.date),
            headers={'Authorization': f'Bearer {self.fitbit_api.auth.get_access_token()}'}
        )

    @patch('requests.get')
    def test_get_steps_data(self, mock_get):
        mock_response = MagicMock()
        expected_data = {'activities-steps': [{'dateTime': self.date, 'value': '10000'}]}
        mock_response.json.return_value = expected_data
        mock_get.return_value = mock_response

        steps_data = self.fitbit_api.get_steps_data(self.date)
        self.assertEqual(steps_data, expected_data)
        mock_get.assert_called_once_with(
            self.fitbit_api.API_URL_STEPS.format(self.date),
            headers={'Authorization': f'Bearer {self.fitbit_api.auth.get_access_token()}'}
        )

    @patch('requests.get')
    def test_get_sleep_data(self, mock_get):
        mock_response = MagicMock()
        expected_data = {'sleep': [{'dateOfSleep': self.date, 'sleepDuration': 28800}]}
        mock_response.json.return_value = expected_data
        mock_get.return_value = mock_response

        sleep_data = self.fitbit_api.get_sleep_data(self.date)
        self.assertEqual(sleep_data, expected_data)
        mock_get.assert_called_once_with(
            self.fitbit_api.API_URL_SLEEP.format(self.date),
            headers={'Authorization': f'Bearer {self.fitbit_api.auth.get_access_token()}'}
        )
