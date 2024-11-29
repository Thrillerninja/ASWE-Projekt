import unittest
from unittest.mock import MagicMock, patch
from datetime import date, timedelta
from usecases.activity_state import ActivityState
import pandas as pd

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
        self.mock_state_machine.preferences = {"sleep_time": "22:00"}

        # Create the ActivityState instance
        self.activity_state = ActivityState(self.mock_state_machine)
        self.pd_to_csv = "pandas.DataFrame.to_csv"
        self.activity_logger_info = "usecases.activity_state.logger.info"

    @patch('usecases.activity_state.ActivityState.calculate_daily_stress_level')
    def test_on_enter_with_stress_level(self, mock_calculate_stress_level):
        """Test the on_enter method when a valid stress level is calculated."""

        # Mock the calculate_daily_stress_level return value
        mock_calculate_stress_level.return_value = "entspannt"
        
        # Mock the Fitbit API response for heart rate data
        self.mock_fitbit_api.get_heart_data.return_value = {
            'activities-heart': [{'value': {'restingHeartRate': 60}}]
        }

        # Mock the TTS API speak method to prevent actual speech
        self.mock_tts_api.speak = MagicMock()

        # Call the on_enter method
        self.activity_state.on_enter()

        # Assert the expected behavior
        self.mock_fitbit_api.get_heart_data.assert_called_once_with(str(date.today()))
        self.mock_tts_api.speak.assert_any_call(
            "Dein Stresslevel wurde heute anhand deiner Herzfrequenz und Aktivitätsdaten analysiert. "
            "Deine Ruheherzfrequenz betrug 60 Schläge pro Minute."
        )
        self.mock_state_machine.activity_idle.assert_called_once()

    @patch('usecases.activity_state.ActivityState.calculate_daily_stress_level')
    def test_on_enter_with_no_stress_level(self, mock_calculate_stress_level):
        """Test the on_enter method when no stress level is found."""

        # Mock the calculate_daily_stress_level return value as None
        mock_calculate_stress_level.return_value = None

        # Mock the TTS API speak method to prevent actual speech
        self.mock_tts_api.speak = MagicMock()

        # Mock missing sleep data (this simulates no sleep data for the last two days)
        self.mock_fitbit_api.get_sleep_data.return_value = {'sleep': []}

        # Call the on_enter method
        self.activity_state.on_enter()

        # Assert that both error messages were spoken
        self.mock_tts_api.speak.assert_any_call("Entschuldigung, ich konnte dein Stresslevel nicht messen.")
        self.mock_tts_api.speak.assert_any_call("Entschuldigung, ich konnte keine Schlafdaten der letzten 2 Tage finden.")
        self.mock_state_machine.activity_idle.assert_called_once()

    @patch('usecases.activity_state.ActivityState.calculate_daily_stress_level')
    @patch('usecases.activity_state.ActivityState.average_sleep_time')
    def test_on_enter_with_sleep_data(self, mock_average_sleep_time, mock_calculate_stress_level):
        """Test the on_enter method when sleep data is available."""

        # Mock the calculate_daily_stress_level return value
        mock_calculate_stress_level.return_value = "entspannt"

        # Mock the Fitbit API response for heart rate data
        self.mock_fitbit_api.get_heart_data.return_value = {
            'activities-heart': [{'value': {'restingHeartRate': 60}}]
        }

        # Mock the trigger_activity_state return value
        mock_average_sleep_time.return_value = 7.5  # Average sleep time in hours

        # Mock the TTS API speak method to prevent actual speech
        self.mock_tts_api.speak = MagicMock()

        # Call the on_enter method
        self.activity_state.on_enter()

        # Assert the expected behavior for sleep data
        mock_average_sleep_time.assert_called_once_with(2)  # 2 days of sleep data
        self.mock_tts_api.speak.assert_any_call("Deine durchschnittliche Schlafzeit der letzten 2 Tage beträgt 7.5.")
        self.mock_state_machine.activity_idle.assert_called_once()

    @patch('usecases.activity_state.ActivityState.calculate_daily_stress_level')
    def test_on_enter_with_no_sleep_data(self, mock_calculate_stress_level):
        """Test the on_enter method when no sleep data is available."""

        # Mock the calculate_daily_stress_level return value
        mock_calculate_stress_level.return_value = "entspannt"

        # Mock the Fitbit API response for heart rate data
        self.mock_fitbit_api.get_heart_data.return_value = {
            'activities-heart': [{'value': {'restingHeartRate': 60}}]
        }

        # Mock the trigger_activity_state return value to None (no sleep data)
        self.mock_state_machine.average_sleep_time.return_value = None

        # Mock the TTS API speak method to prevent actual speech
        self.mock_tts_api.speak = MagicMock()

        # Call the on_enter method
        self.activity_state.on_enter()

        # Assert the expected behavior for no sleep data
        self.mock_tts_api.speak.assert_any_call("Entschuldigung, ich konnte keine Schlafdaten der letzten 2 Tage finden.")
        self.mock_state_machine.activity_idle.assert_called_once()

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

        # Mock pandas DataFrame to_csv method to prevent file creation
        with patch(self.pd_to_csv):
            # Call the method
            stress_level = self.activity_state.calculate_daily_stress_level(date.today().strftime('%Y-%m-%d'))

            # Assert the result
            self.assertEqual(stress_level, "entspannt")
            self.mock_fitbit_api.get_heart_data.assert_called_once()
            self.mock_fitbit_api.get_steps_data.assert_called_once()

            # Ensure to_csv was not called (indicating that no CSV file was created)
            #mock_to_csv.assert_not_called()

    def test_calculate_daily_stress_level_very_relaxed(self):
        """Test the stress level calculation when the user is very relaxed."""
        # Mock Fitbit API responses for very relaxed state
        self.mock_fitbit_api.get_heart_data.return_value = {
            'activities-heart': [{'value': {'restingHeartRate': 60}}],  
            'activities-heart-intraday': {
                'dataset': [{'time': '12:00', 'value': 45}]  # Niedrigere Herzfrequenz
            }
        }
        self.mock_fitbit_api.get_steps_data.return_value = {
            'activities-steps-intraday': {
                'dataset': [{'time': '12:00', 'value': 20}]  # Sehr niedrige Schritte (zeigt Entspannung)
            }
        }

        with patch(self.pd_to_csv):
            # Call the method
            stress_level = self.activity_state.calculate_daily_stress_level(date.today().strftime('%Y-%m-%d'))

            # Assert the result
            self.assertEqual(stress_level, "sehr entspannt")
            self.mock_fitbit_api.get_heart_data.assert_called_once()
            self.mock_fitbit_api.get_steps_data.assert_called_once()
            # Ensure to_csv was not called (indicating that no CSV file was created)
            #mock_to_csv.assert_not_called()

    def test_calculate_daily_stress_level_stressed(self):
        """Test the stress level calculation when the user is stressed."""
        # Mock Fitbit API responses for stressed state
        self.mock_fitbit_api.get_heart_data.return_value = {
            'activities-heart': [{'value': {'restingHeartRate': 60}}],  
            'activities-heart-intraday': {
                'dataset': [{'time': '12:00', 'value': 85}]  # High heart rate
            }
        }
        self.mock_fitbit_api.get_steps_data.return_value = {
            'activities-steps-intraday': {
                'dataset': [{'time': '12:00', 'value': 20}]  
            }
        }

        with patch(self.pd_to_csv):
            # Call the method
            stress_level = self.activity_state.calculate_daily_stress_level(date.today().strftime('%Y-%m-%d'))

            # Assert the result
            self.assertEqual(stress_level, "gestresst")
            self.mock_fitbit_api.get_heart_data.assert_called_once()
            self.mock_fitbit_api.get_steps_data.assert_called_once()
            # Ensure to_csv was not called (indicating that no CSV file was created)
            #mock_to_csv.assert_not_called()

    def test_trigger_activity_state_average_sleep_time(self):
        """Test the average sleep time calculation."""
        # Mock Fitbit API responses for two days
        self.mock_fitbit_api.get_sleep_data.side_effect = [
            {'sleep': [{'isMainSleep': True, 'startTime': '2023-11-27T22:30:00.000'}]},
            {'sleep': [{'isMainSleep': True, 'startTime': '2023-11-26T23:00:00.000'}]},
        ]

        # Call the method
        avg_sleep_time = self.activity_state.average_sleep_time(days=2)

        # Assert the result
        self.assertEqual(avg_sleep_time, "22:45")
        self.assertEqual(self.mock_fitbit_api.get_sleep_data.call_count, 2)

    def test_suggest_music_stressed(self):
        """Test the music suggestion for a stressed user."""
        # Mock the TTS API responses
        self.mock_tts_api.ask_yes_no.return_value = True

        # Call the method
        with patch(self.activity_logger_info):
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

    def test_calculate_daily_stress_level_error(self):
        """Test the stress level calculation when an error occurs (e.g., missing steps data)."""
        # Mock Fitbit API responses
        self.mock_fitbit_api.get_heart_data.return_value = {
            'activities-heart': [{'value': {'restingHeartRate': 60}}],
            'activities-heart-intraday': {
                'dataset': [{'time': '12:00', 'value': 65}]
            }
        }

        # Mock missing steps data to simulate an error case
        self.mock_fitbit_api.get_steps_data.return_value = None

        # Call the method
        stress_level = self.activity_state.calculate_daily_stress_level(date.today().strftime('%Y-%m-%d'))

        # Assert that no stress level could be calculated due to missing steps data
        self.assertIsNone(stress_level)
        self.mock_fitbit_api.get_heart_data.assert_called_once()
        self.mock_fitbit_api.get_steps_data.assert_called_once()

    def test_calculate_daily_stress_level_no_inactive_phases(self):
        """Test the stress level calculation when no inactive phases are found."""
        # Mock Fitbit API responses
        self.mock_fitbit_api.get_heart_data.return_value = {
            'activities-heart': [{'value': {'restingHeartRate': 60}}],  # Resting heart rate
            'activities-heart-intraday': {
                'dataset': [{'time': '12:00', 'value': 65}]  # Heart rate data
            }
        }
        self.mock_fitbit_api.get_steps_data.return_value = {
            'activities-steps-intraday': {
                'dataset': [{'time': '12:00', 'value': 100}]  # No inactive phases (steps > 60)
            }
        }

        # Mock pandas DataFrame to_csv method to prevent file creation
        with patch(self.pd_to_csv):
            # Call the method
            stress_level = self.activity_state.calculate_daily_stress_level(date.today().strftime('%Y-%m-%d'))

            # Assert the result
            self.assertIsNone(stress_level)  # No inactive phases, so the return value should be None
            self.mock_fitbit_api.get_heart_data.assert_called_once()  # Ensure Fitbit API was called
            self.mock_fitbit_api.get_steps_data.assert_called_once()  # Ensure steps data was fetched


    def test_suggest_music_relaxed(self):
        """Test the music suggestion for a relaxed user."""
        # Mock the TTS API responses
        self.mock_tts_api.ask_yes_no.return_value = True

        # Call the method
        with patch(self.activity_logger_info):
            self.activity_state.suggest_music("entspannt")

        # Assert TTS interactions
        self.mock_tts_api.speak.assert_any_call("Du warst heute in einem guten, entspannten Zustand. Musik könnte den Abend noch besser machen.")
        self.mock_tts_api.ask_yes_no.assert_called_once_with("Möchtest du die Musik abspielen?")

    def test_suggest_music_no_playback(self):
        """Test that no music is played when the user declines."""
        # Mock the TTS API responses
        self.mock_tts_api.ask_yes_no.return_value = False

        # Call the method
        with patch(self.activity_logger_info):
            self.activity_state.suggest_music("gestresst")

        # Assert TTS interactions
        self.mock_tts_api.speak.assert_any_call("Okay, gute Nacht!")
        self.mock_tts_api.ask_yes_no.assert_called_once_with("Möchtest du die Musik abspielen?")

    def test_no_playlist_found(self):
        """Test the case when no playlist is found for the stress category."""
        
        # Setze einen ungültigen Stresskategorie-Wert, der keine Playlist zugeordnet hat
        stress_category = "unbekannt"  # Ein Wert, der keine Playlist zugeordnet hat
        
        # Rufe die Methode suggest_music auf
        self.activity_state.suggest_music(stress_category)
        
        # Überprüfe, dass die TTS-API die entsprechende Fehlermeldung ausgesprochen hat
        self.mock_tts_api.speak.assert_called_once_with("Entschuldigung, ich konnte keine passende Playlist finden.")
        
        self.mock_tts_api.ask_yes_no.assert_not_called()

    @patch('usecases.activity_state.datetime')
    def test_check_trigger_activity_time_matches(self, mock_datetime):
        """Test that goto_activity is called when current time matches the sleep time and last_activated_at is different."""
        mock_now = MagicMock()
        mock_now.strftime.return_value = "2024-11-29 22:00"
        mock_datetime.datetime.now.return_value = mock_now

        self.activity_state.last_activated_at = "2024-11-29 21:00"

        self.activity_state.check_trigger_activity()
        self.mock_state_machine.goto_activity.assert_called_once()


    @patch('usecases.activity_state.datetime')
    def test_check_trigger_activity_does_not_enter_if(self, mock_datetime):
        """Test that goto_activity is NOT called when current time does not match or last_activated_at is the same."""
        mock_now = MagicMock()
        mock_now.strftime.return_value = "2024-11-29 20:00"
        mock_datetime.datetime.now.return_value = mock_now

        self.activity_state.last_activated_at = "2024-11-29 20:00"

        self.activity_state.check_trigger_activity()
        self.mock_state_machine.goto_activity.assert_not_called()

