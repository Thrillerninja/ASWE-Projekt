import unittest
from unittest.mock import MagicMock, patch
from datetime import date, timedelta
from usecases.activity_state import ActivityState

class TestActivityState(unittest.TestCase):

    def setUp(self):
        """Set up the mocks and the instance of ActivityState."""
        # Mock the state_machine and its API factory
        self.mock_state_machine = MagicMock()
        self.mock_fitbit_api = MagicMock()
        self.mock_tts_api = MagicMock()
        self.mock_spotify_api = MagicMock()

        # Configure the API factory to return mocked APIs
        self.mock_state_machine.api_factory.create_api.side_effect = lambda api_type: {
            "fitbit": self.mock_fitbit_api,
            "tts": self.mock_tts_api,
            "spotify": self.mock_spotify_api
        }[api_type]

        # Create the ActivityState instance
        self.activity_state = ActivityState(self.mock_state_machine)

    def test_calculate_daily_stress_level_relaxed(self):
        """Test the stress level calculation when the user is relaxed."""
        # Mock Fitbit API responses
        self.mock_fitbit_api.get_heart_data.return_value = {
            'activities-heart': [{'value': {'restingHeartRate': 60}}],
            'activities-heart-intraday': {
                'dataset': [{'time': '12:00', 'value': 65}]
            }
        }
        self.mock_fitbit_api.get_steps_data.return_value = {
            'activities-steps-intraday': {
                'dataset': [{'time': '12:00', 'value': 50}]
            }
        }

        # Call the method
        stress_level = self.activity_state.calculate_daily_stress_level(date.today().strftime('%Y-%m-%d'))

        # Assert the result
        self.assertEqual(stress_level, "entspannt")
        self.mock_fitbit_api.get_heart_data.assert_called_once()
        self.mock_fitbit_api.get_steps_data.assert_called_once()

    def test_trigger_activity_state_average_sleep_time(self):
        """Test the average sleep time calculation."""
        # Mock Fitbit API responses for two days
        self.mock_fitbit_api.get_sleep_data.side_effect = [
            {'sleep': [{'isMainSleep': True, 'startTime': '2023-11-27T22:30:00.000'}]},
            {'sleep': [{'isMainSleep': True, 'startTime': '2023-11-26T23:00:00.000'}]},
        ]

        # Call the method
        avg_sleep_time = self.activity_state.trigger_activity_state(days=2)

        # Assert the result
        self.assertEqual(avg_sleep_time, "22:45")
        self.assertEqual(self.mock_fitbit_api.get_sleep_data.call_count, 2)

    def test_suggest_music_stressed(self):
        """Test the music suggestion for a stressed user."""
        # Mock the TTS API responses
        self.mock_tts_api.ask_yes_no.return_value = True

        # Call the method
        with patch("usecases.activity_state.logger.info") as mock_logger:
            self.activity_state.suggest_music("gestresst")

        # Assert TTS interactions
        self.mock_tts_api.speak.assert_any_call("Du scheinst heute gestresst gewesen zu sein. "
                                                "Entspannende Musik könnte helfen, vor dem Schlafen abzuschalten.")
        self.mock_tts_api.ask_yes_no.assert_called_once_with("Möchtest du die Musik abspielen?")

    def test_get_sleep_start_time(self):
        """Test retrieving the sleep start time."""
        # Mock Fitbit API response
        self.mock_fitbit_api.get_sleep_data.return_value = {
            'sleep': [{'isMainSleep': True, 'startTime': '2023-11-27T23:15:00.000'}]
        }

        # Call the method
        sleep_start_time = self.activity_state.get_sleep_start_time(date.today().strftime('%Y-%m-%d'))

        # Assert the result
        self.assertEqual(sleep_start_time, "23:15")
        self.mock_fitbit_api.get_sleep_data.assert_called_once()

    def test_get_sleep_start_time_no_data(self):
        """Test retrieving sleep start time when no data is available."""
        # Mock Fitbit API response
        self.mock_fitbit_api.get_sleep_data.return_value = {'sleep': []}

        # Call the method
        sleep_start_time = self.activity_state.get_sleep_start_time(date.today().strftime('%Y-%m-%d'))

        # Assert the result
        self.assertIsNone(sleep_start_time)
        self.mock_fitbit_api.get_sleep_data.assert_called_once()

