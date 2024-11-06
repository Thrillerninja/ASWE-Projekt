import datetime
import unittest
from unittest.mock import patch, MagicMock
from usecases.welcome_state import WelcomeState
from usecases.state_machine import StateMachine

class TestWelcomeState(unittest.TestCase):

    @patch('usecases.welcome_state.WelcomeState.calc_alarm_time', return_value=datetime.time(7, 0))
    def test_on_enter(self, mock_calc_alarm_time):
        state_machine = StateMachine()
        welcome_state = WelcomeState(state_machine)

        # Mock APIs
        welcome_state.tts_api = MagicMock()
        welcome_state.weather_api = MagicMock()
        welcome_state.rapla_api = MagicMock()

        # Mock API responses
        welcome_state.weather_api.get_daily_forecast.return_value = {'min_temp': 10, 'max_temp': 20, 'avg_condition': 'sunny'}
        welcome_state.weather_api.get_weather.return_value = {'main': {'temp': 15}}
        welcome_state.rapla_api.get_todays_appointments.return_value = []

        welcome_state.on_enter()

        # Check if TTS API was called with the correct message
        welcome_state.tts_api.speak.assert_any_call("Guten Morgen! Es ist ")
        welcome_state.tts_api.speak.assert_any_call("Die Wettervorhersage für heute: Die Temperatur wird zwischen 10°C und 20°C liegen.")
        welcome_state.tts_api.speak.assert_any_call("Im Moment sind es 15°C.")
        welcome_state.tts_api.speak.assert_any_call("Sie haben heute keine Termine.")

if __name__ == '__main__':
    unittest.main()
