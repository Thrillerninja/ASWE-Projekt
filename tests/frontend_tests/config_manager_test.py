import unittest
from unittest.mock import MagicMock, patch
import json
from PyQt5.QtCore import QTime
from frontend.config_manager import ConfigManager

class TestConfigManager(unittest.TestCase):

    def setUp(self):
        """Set up the test environment."""
        self.mock_view = MagicMock()
        self.mock_view.ui = MagicMock()
        
        self.config_manager = ConfigManager(self.mock_view)

        self.config_manager.preferences = {
            'fuel_type': 'super-e10',
            'default_alarm_time': '08:00',
            'sleep_time': '22:00',
            'fuel_threshold': 1.5
        }

    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_load_preferences_file(self, mock_open):
        """Test loading preferences from a file."""
        # Simulate loading preferences
        mock_open.return_value.read.return_value = """{
            "fuel_type": "diesel",
            "fuel_threshold": 2.0,
            "default_alarm_time": "00:00",
            "sleep_time": "00:00",
            "home_location": {
                "name": "asperg",
                "vvs_code": "de:08118:7400",
                "address": {
                    "street": "Alleenstra\u00c3\u0178e",
                    "number": "1",
                    "zipcode": "71679",
                    "city": "Asperg",
                    "country": "Germany"
                },
                "coordinates": {
                    "latitude": 48.907256,
                    "longitude": 9.147977
                }
            },
            "default_destination": {
                "name": "dhbw",
                "vvs_code": "de:08111:6072",
                "address": {
                    "street": "Lerchenstra\u00c3\u0178e",
                    "number": "1",
                    "zipcode": "70174",
                    "city": "Stuttgart",
                    "country": "Germany"
                },
                "coordinates": {
                    "latitude": 48.7826,
                    "longitude": 9.167025
                }
            }
        }"""

        self.config_manager.load_preferences_file()

        self.assertEqual(self.config_manager.preferences['fuel_type'], 'diesel')
        self.assertEqual(self.config_manager.preferences['fuel_threshold'], 2.0)
        self.assertEqual(self.config_manager.preferences['default_alarm_time'], '00:00')
        self.assertEqual(self.config_manager.preferences['sleep_time'], '00:00')

        self.assertEqual(self.config_manager.preferences['home_location']['name'], 'asperg')
        self.assertEqual(self.config_manager.preferences['home_location']['address']['city'], 'Asperg')
        self.assertEqual(self.config_manager.preferences['default_destination']['coordinates']['latitude'], 48.7826)

        mock_open.assert_called_once_with(self.config_manager.preferences_file, 'r')

    @patch('builtins.open', side_effect=FileNotFoundError)
    def test_load_preferences_file_file_not_found(self, mock_open):
        """Test handling of missing preferences file."""
        self.config_manager.load_preferences_file()
        self.assertEqual(self.config_manager.preferences, {})

    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_load_preferences_file_json_decode_error(self, mock_open):
        """Test handling of invalid JSON in preferences file."""
        mock_open.return_value.read.return_value = "{invalid_json: true}"

        with patch('json.load', side_effect=json.JSONDecodeError("Expecting value", "document", 0)):
            self.config_manager.load_preferences_file()

        self.assertEqual(self.config_manager.preferences, {})

    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_save_preferences(self, mock_open):
        """Test saving preferences to a file."""
        
        self.config_manager.save_preferences()

        mock_open.assert_called_once_with(self.config_manager.preferences_file, 'w')
        
        written_data = ''.join(call[0][0] for call in mock_open.return_value.write.call_args_list)
        written_json = json.loads(written_data)

        expected_json = {
            "fuel_type": "super-e10",
            "default_alarm_time": "08:00",
            "sleep_time": "22:00",
            "fuel_threshold": 1.5
        }

        self.assertEqual(written_json, expected_json)

    def test_update_preference(self):
        """Test updating preferences."""
        self.config_manager.update_preference('fuel_type', 'super-plus')
        self.config_manager.update_preference('fuel_threshold', 1.34)
        self.config_manager.update_preference('default_alarm_time', '07:00')
        self.config_manager.update_preference('sleep_time', '21:00')

        self.assertEqual(self.config_manager.preferences['fuel_type'], 'super-plus')
        self.assertEqual(self.config_manager.preferences['fuel_threshold'], 1.34)
        self.assertEqual(self.config_manager.preferences['default_alarm_time'], '07:00')
        self.assertEqual(self.config_manager.preferences['sleep_time'], '21:00')

    def test_get_preference(self):
        """Test getting preferences."""
        fuel_type = self.config_manager.get_preference('fuel_type')
        fuel_threshold = self.config_manager.get_preference('fuel_threshold')
        default_alarm_time = self.config_manager.get_preference('default_alarm_time')
        sleep_time = self.config_manager.get_preference('sleep_time')

        self.assertEqual(fuel_type, 'super-e10')
        self.assertEqual(fuel_threshold, 1.5)
        self.assertEqual(default_alarm_time, '08:00')
        self.assertEqual(sleep_time, '22:00')

    def test_set_initial_values(self):
        """Test setting initial values based on preferences."""
        # Mock the view methods to test if they are called with correct values
        self.config_manager.set_initial_values()

        self.mock_view.set_cb_fuel_type.assert_called_with(0)

        self.mock_view.set_te_default_alarm_time.assert_called_with(QTime.fromString('08:00', "hh:mm"))
        self.mock_view.set_te_sleep_time.assert_called_with(QTime.fromString('22:00', "hh:mm"))

        self.mock_view.set_sl_fuel_threshold.assert_called_with(150)
        self.mock_view.set_le_fuel_threshold.assert_called_with('1.50')

    def test_on_cb_fuel_type_changed(self):
        """Test fuel type change handling."""
        self.config_manager.on_cb_fuel_type_changed(1)

        self.assertEqual(self.config_manager.preferences['fuel_type'], 'super-e5')

    def test_on_time_changed(self):
        """Test time change handling."""
        alarm_time = QTime.fromString('10:30', 'hh:mm')
        sleep_time = QTime.fromString('14:30', 'hh:mm')

        self.config_manager.on_time_changed('default_alarm_time', alarm_time)
        self.config_manager.on_time_changed('sleep_time', sleep_time)

        self.assertEqual(self.config_manager.preferences['default_alarm_time'], '10:30')
        self.assertEqual(self.config_manager.preferences['sleep_time'], '14:30')

    def test_on_sl_fuel_threshold_changed(self):
        """Test fuel threshold slider change handling."""
        self.config_manager.on_sl_fuel_threshold_changed(175)

        self.assertEqual(self.config_manager.preferences['fuel_threshold'], 1.75)
        self.mock_view.set_le_fuel_threshold.assert_called_with('1.75')

    @patch('frontend.config_manager.ConfigManager.update_preference')
    def test_on_le_fuel_threshold_changed_valid(self, mock_update):
        """Test valid fuel threshold input handling."""
        self.config_manager.on_le_fuel_threshold_changed("1.75")

        mock_update.assert_called_with('fuel_threshold', 1.75)
        self.mock_view.set_sl_fuel_threshold.assert_called_with(175)

    @patch('frontend.config_manager.ConfigManager.update_preference')
    def test_on_le_fuel_threshold_changed_invalid(self, mock_update):
        """Test invalid fuel threshold input handling."""
        self.config_manager.on_le_fuel_threshold_changed("abc")

        self.mock_view.show_error_le_fuel_threshold.assert_called_with("Fuel threshold must be a number between 1.00 and 2.00")

    @patch('frontend.config_manager.ConfigManager.update_preference')
    def test_on_le_fuel_threshold_changed_currency_symbol(self, mock_update):
        """Test fuel threshold input with currency symbol."""
        self.config_manager.on_le_fuel_threshold_changed("1.50 €")

        mock_update.assert_called_with('fuel_threshold', 1.50)
        self.mock_view.set_sl_fuel_threshold.assert_called_with(150)
        self.mock_view.set_le_fuel_threshold.assert_called_with("1.50")

    @patch('frontend.config_manager.ConfigManager.update_preference')
    def test_on_le_fuel_threshold_changed_out_of_range(self, mock_update):
        """Test fuel threshold input outside valid range."""
        # below minimum range
        self.config_manager.on_le_fuel_threshold_changed("0.99")
        self.mock_view.show_error_le_fuel_threshold.assert_called_with("Fuel threshold must be a number between 1.00 and 2.00")

        # above maximum range
        self.config_manager.on_le_fuel_threshold_changed("2.01")
        self.mock_view.show_error_le_fuel_threshold.assert_called_with("Fuel threshold must be a number between 1.00 and 2.00")

if __name__ == '__main__':
    unittest.main()
