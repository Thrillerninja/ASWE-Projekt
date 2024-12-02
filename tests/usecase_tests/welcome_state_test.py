import datetime
import unittest
from unittest.mock import patch, MagicMock
from usecases.welcome_state import WelcomeState
from api.api_factory import APIFactory

class TestWelcomeState(unittest.TestCase):
    @patch.object(APIFactory, 'create_api')
    def test_on_enter(self, mock_create_api):
        # Mock APIs
        mock_tts_api = MagicMock()
        mock_weather_api = MagicMock()
        mock_rapla_api = MagicMock()
        
        mock_create_api.side_effect = lambda api_type, state_machine=None: {
            "tts": mock_tts_api,
            "weather": mock_weather_api,
            "rapla": mock_rapla_api
        }[api_type]
        
        # Mock API responses
        mock_weather_api.get_daily_forecast.return_value = {'min_temp': 10, 'max_temp': 20, 'avg_condition': 'sunny'}
        mock_weather_api.get_weather.return_value = {'main': {'temp': 15}}
        mock_rapla_api.get_todays_appointments.return_value = []

        # Mock preferences
        mock_preferences = {
            "enable_elevenlabs": 0
        }

        # Initialize WelcomeState
        state_machine = MagicMock()
        mock_config = MagicMock()  # Mock configuration
        state_machine.api_factory = APIFactory(mock_config)
        state_machine.preferences = mock_preferences
        welcome_state = WelcomeState(state_machine)
        
        # Call on_enter
        welcome_state.on_enter()

        # Check if TTS API was called with the correct message
        mock_tts_api.speak.assert_any_call(f"Guten Morgen! Es ist {datetime.datetime.now().strftime('%H:%M')}. Die Wettervorhersage für heute: Die Temperatur wird zwischen 10 und 20 Grad Celsius liegen und sunny Im Moment sind es 15 Grad Celsius.")
        mock_tts_api.speak.assert_any_call("Sie haben heute keine Termine.")
        
class TestAlarm(unittest.TestCase):
    def setUp(self):
        # Mock the state machine and API factory
        self.state_machine = MagicMock()
        self.state_machine.api_factory = MagicMock()
        self.state_machine.preferences = {"default_alarm_time": "09:00"}
        
        # Mock the create_api method to return a mock RaplaAPI instance
        self.mock_rapla_api = MagicMock()
        self.state_machine.api_factory.create_api.return_value = self.mock_rapla_api
        
        # Initialize WelcomeState
        self.welcome_state = WelcomeState(self.state_machine)
        
        # Set default wakeup time
        self.welcome_state.default_wakeup_time = datetime.time(9, 0)

    def test_calc_alarm_time_no_appointments(self):
        # Mock no calendar entries
        self.mock_rapla_api.get_todays_appointments.return_value = []
        
        # Call calc_alarm_time
        alarm_time = self.welcome_state.calc_alarm_time()
        
        # Assert the alarm time is set to the default wakeup time
        self.assertEqual(alarm_time, self.welcome_state.default_wakeup_time)

    def test_calc_alarm_time_with_appointments(self):
        # Mock calendar entries
        appointment = MagicMock()
        appointment.start = "8:00"
        appointment.date = "01.01.2023"
        self.mock_rapla_api.get_todays_appointments.return_value = [appointment]
        
        # Mock transit time
        transit_time = 30  # 30 minutes
        self.state_machine.api_factory.create_api.return_value.calc_trip_time.return_value = transit_time
        
        # Call calc_alarm_time
        alarm_time = self.welcome_state.calc_alarm_time()
        
        # Calculate expected alarm time
        first_appointment_time = datetime.datetime.strptime(appointment.start, "%H:%M").time()
        first_appointment_date = datetime.datetime.strptime(appointment.date, "%d.%m.%Y")
        first_appointment_datetime = datetime.datetime.combine(first_appointment_date, first_appointment_time)
        expected_alarm_time = (first_appointment_datetime - datetime.timedelta(minutes=transit_time)).time()
        
        # Assert the alarm time is calculated correctly
        self.assertEqual(alarm_time, expected_alarm_time)

    def test_calc_alarm_time_late_appointment(self):
        # Mock calendar entries
        appointment = MagicMock()
        appointment.start = "11:00"
        appointment.date = "01.01.2023"
        self.mock_rapla_api.get_todays_appointments.return_value = [appointment]
        
        # Mock transit time
        transit_time = 30  # 30 minutes
        self.state_machine.api_factory.create_api.return_value.calc_trip_time.return_value = transit_time
        
        # Call calc_alarm_time
        alarm_time = self.welcome_state.calc_alarm_time()
        
        # Assert the alarm time is set to the default wakeup time
        self.assertEqual(alarm_time, self.welcome_state.default_wakeup_time)
