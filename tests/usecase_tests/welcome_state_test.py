import unittest
from unittest.mock import MagicMock
from usecases.welcome_state import WelcomeState
from datetime import datetime

class TestWelcomeState(unittest.TestCase):

    def setUp(self):
        self.state_machine = MagicMock()
        self.welcome_state = WelcomeState(self.state_machine)

    def test_on_enter(self):
        self.welcome_state.calc_alarm_time = MagicMock(return_value=datetime.time(7, 0))
        self.welcome_state.weather_api.get_daily_forecast = MagicMock(return_value={
            'min_temp': 10,
            'max_temp': 20,
            'avg_condition': 'clear sky'
        })
        self.welcome_state.weather_api.get_weather = MagicMock(return_value={
            'main': {'temp': 15}
        })
        self.welcome_state.rapla_api.get_todays_appointments = MagicMock(return_value=[
            MagicMock(start='09:00', room='Room 101')
        ])
        self.welcome_state.tts_api.speak = MagicMock()
        self.welcome_state.tts_api.ask_yes_no = MagicMock(return_value=True)

        self.welcome_state.on_enter()

        self.welcome_state.tts_api.speak.assert_called()
        self.welcome_state.tts_api.ask_yes_no.assert_called()