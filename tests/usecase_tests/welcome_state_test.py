import unittest
from unittest.mock import MagicMock
from usecases.welcome_state import WelcomeState
from datetime import datetime, time

class TestWelcomeState(unittest.TestCase):

    def setUp(self):
        self.state_machine = MagicMock()
        self.welcome_state = WelcomeState(self.state_machine)
        self.welcome_state.state_machine.morning_news = MagicMock()
        self.welcome_state.state_machine.interaction = MagicMock()
        self.welcome_state.state_machine.morning_news.on_enter = MagicMock()
        self.welcome_state.state_machine.interaction.on_enter = MagicMock()

    def test_on_enter(self):
        self.welcome_state.calc_alarm_time = MagicMock(return_value=time(7, 0))
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
        self.welcome_state.state_machine.morning_news.assert_called()
        self.welcome_state.state_machine.morning_news.on_enter.assert_not_called()
        self.welcome_state.state_machine.interaction.on_enter.assert_not_called()