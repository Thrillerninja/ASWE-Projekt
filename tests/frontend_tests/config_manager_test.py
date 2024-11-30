import unittest
from unittest.mock import MagicMock, patch, mock_open
import json
from PyQt5.QtCore import QTime
from frontend.config_manager import ConfigManager, load_preferences_file, PREFERENCES_FILE
import speech_recognition as sr

class TestConfigManager(unittest.TestCase):

    def setUp(self):
        """Set up the test environment."""
        patcher_get_active_mics = patch('frontend.config_manager.ConfigManager.get_active_mics', return_value=[[1, 'Mic 1'], [7, 'Mic 7']])
        patcher_get_active_mics.start()
        self.addCleanup(patcher_get_active_mics.stop)

        self.mock_view = MagicMock()
        self.mock_view.ui = MagicMock()
        self.mock_view.state_machine = MagicMock()
        
        self.config_manager = ConfigManager(self.mock_view)

        self.config_manager.preferences = {
            'fuel_type': 'super-e10',
            'default_alarm_time': '08:00',
            'sleep_time': '22:00',
            'fuel_threshold': 1.5,
            'fuel_demo_price': 0.0,
        }

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
            "fuel_threshold": 1.5,
            'fuel_demo_price': 0.0
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
        self.config_manager.preferences['mic_id'] = 1
        # Mock the active microphones list as defined in the setup
        self.config_manager.active_mics = [[0, 'Mic 0'], [1, 'Mic 1'], [7, 'Mic 7']]

        # Mock the set methods on the view
        self.mock_view.set_cb_fuel_type = MagicMock()
        self.mock_view.set_te_default_alarm_time = MagicMock()
        self.mock_view.set_te_sleep_time = MagicMock()
        self.mock_view.set_sl_fuel_threshold = MagicMock()
        self.mock_view.set_le_fuel_threshold = MagicMock()
        self.mock_view.set_mic_list = MagicMock()
        self.mock_view.set_mic_id = MagicMock()

        # Call the method to test
        self.config_manager.set_initial_values()

        # Ensure the view methods are called with correct values from preferences
        self.mock_view.set_cb_fuel_type.assert_called_with(0)  # Assuming 'super-e10' is the first fuel type
        self.mock_view.set_te_default_alarm_time.assert_called_with(QTime.fromString('08:00', "hh:mm"))
        self.mock_view.set_te_sleep_time.assert_called_with(QTime.fromString('22:00', "hh:mm"))
        self.mock_view.set_sl_fuel_threshold.assert_called_with(150)  # 1.5 * 100
        self.mock_view.set_le_fuel_threshold.assert_called_with('1.50')
        self.mock_view.set_mic_list.assert_called_with(self.config_manager.active_mics)
        self.mock_view.set_mic_id.assert_called_with(1)

    def test_set_initial_values_fallback_mic_id(self):
        """Test when the selected microphone ID is not in the active microphones list."""
        # Mock the preferences with a mic_id that doesn't exist in active_mics
        self.config_manager.preferences['mic_id'] = 99  # Invalid mic_id

        # Mock the active microphones list (no mic with ID 99)
        self.config_manager.active_mics = [[0, 'Mic 0'], [1, 'Mic 1'], [7, 'Mic 7']]

        # Mock the set methods on the view
        self.mock_view.set_cb_fuel_type = MagicMock()
        self.mock_view.set_te_default_alarm_time = MagicMock()
        self.mock_view.set_te_sleep_time = MagicMock()
        self.mock_view.set_sl_fuel_threshold = MagicMock()
        self.mock_view.set_le_fuel_threshold = MagicMock()
        self.mock_view.set_mic_list = MagicMock()
        self.mock_view.set_mic_id = MagicMock()

        # Call the method to test
        self.config_manager.set_initial_values()

        # Ensure the mic_id preference is updated to the first available mic (ID 0)
        self.mock_view.set_mic_id.assert_called_with(0)
        self.mock_view.set_mic_list.assert_called_with(self.config_manager.active_mics)
        self.mock_view.state_machine.preferences['mic_id'] = 0

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

    @patch('frontend.config_manager.ConfigManager.update_preference')
    def test_on_le_fuel_demo_price_changed_valid(self, mock_update):
        """Test valid fuel threshold input handling."""
        self.config_manager.on_le_fuel_demo_price_changed("1.75")

        mock_update.assert_called_with('fuel_demo_price', 1.75)

    @patch('frontend.config_manager.ConfigManager.update_preference')
    def test_on_le_fuel_demo_price_changed_invalid(self, mock_update):
        """Test invalid fuel threshold input handling."""
        self.config_manager.on_le_fuel_demo_price_changed("abc")

        self.mock_view.show_error_le_fuel_demo_price.assert_called_with("Fuel demo price must be a number")

class TestConvertTextToFloat(unittest.TestCase):

    def setUp(self):
        # Create a mock view and initialize ConfigManager with it
        patcher_get_active_mics = patch('frontend.config_manager.ConfigManager.get_active_mics', return_value=[[1, 'Mic 1'], [7, 'Mic 7']])
        patcher_get_active_mics.start()
        self.addCleanup(patcher_get_active_mics.stop)

        self.mock_view = MagicMock()
        self.mock_view.ui = MagicMock()
        self.config_manager = ConfigManager(self.mock_view)

    def test_convert_valid_float_with_dot(self):
        """Test valid float input with dot notation."""
        result = self.config_manager.convert_text_to_float("123.45")
        self.assertEqual(result, 123.45)

    def test_convert_valid_float_with_comma(self):
        """Test valid float input with comma notation."""
        result = self.config_manager.convert_text_to_float("123,45")
        self.assertEqual(result, 123.45)

    def test_convert_text_with_trailing_space(self):
        """Test valid float input with leading/trailing spaces."""
        result = self.config_manager.convert_text_to_float("  123.45  ")
        self.assertEqual(result, 123.45)

    def test_convert_text_with_trailing_euro_symbol(self):
        """Test text with ' €' at the end of the number."""
        result = self.config_manager.convert_text_to_float("123.45 €")
        self.assertEqual(result, 123.45)

    def test_convert_text_with_comma_and_euro_symbol(self):
        """Test text with a comma and ' €' at the end."""
        result = self.config_manager.convert_text_to_float("123,45 €")
        self.assertEqual(result, 123.45)

    def test_invalid_input_with_non_numeric_characters(self):
        """Test invalid input that can't be converted to a float."""
        result = self.config_manager.convert_text_to_float("abc")
        self.assertEqual(result, -1)

    def test_empty_input(self):
        """Test empty input."""
        result = self.config_manager.convert_text_to_float("")
        self.assertEqual(result, -1)

    def test_only_euro_symbol(self):
        """Test input that only contains ' €'."""
        result = self.config_manager.convert_text_to_float(" €")
        self.assertEqual(result, -1)

    def test_only_comma(self):
        """Test input with just a comma."""
        result = self.config_manager.convert_text_to_float(",")
        self.assertEqual(result, -1)

    def test_only_dot(self):
        """Test input with just a dot."""
        result = self.config_manager.convert_text_to_float(".")
        self.assertEqual(result, -1)

class TestLoadPreferencesFile(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open)
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
                    "street": "Alleenstraße",
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
                    "street": "Lerchenstraße",
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

        preferences = load_preferences_file()

        self.assertEqual(preferences['fuel_type'], 'diesel')
        self.assertEqual(preferences['fuel_threshold'], 2.0)
        self.assertEqual(preferences['default_alarm_time'], '00:00')
        self.assertEqual(preferences['sleep_time'], '00:00')

        self.assertEqual(preferences['home_location']['name'], 'asperg')
        self.assertEqual(preferences['home_location']['address']['city'], 'Asperg')
        self.assertEqual(preferences['default_destination']['coordinates']['latitude'], 48.7826)

        mock_open.assert_called_once_with(PREFERENCES_FILE, 'r')

    @patch('builtins.open', side_effect=FileNotFoundError)
    def test_load_preferences_file_file_not_found(self, mock_open):
        """Test handling of missing preferences file."""
        preferences = load_preferences_file()
        self.assertEqual(preferences, {})

    @patch('builtins.open', new_callable=mock_open)
    def test_load_preferences_file_json_decode_error(self, mock_open):
        """Test handling of invalid JSON in preferences file."""
        mock_open.return_value.read.return_value = "{invalid_json: true}"

        with patch('json.load', side_effect=json.JSONDecodeError("Expecting value", "document", 0)):
            preferences = load_preferences_file()

        self.assertEqual(preferences, {})

class TestConfigManagerMicFunctions(unittest.TestCase):

    @patch('speech_recognition.Microphone.list_microphone_names')
    @patch('speech_recognition.Microphone')
    def test_get_active_mics(self, mock_microphone, mock_list_microphone_names):
        # Mock the microphones list returned by `list_microphone_names`
        mock_list_microphone_names.return_value = ['Mic 1', 'Mic 2', 'Mic 3']

        # Mock the `Microphone` instance behavior
        mock_microphone_instance = MagicMock()
        mock_microphone.return_value = mock_microphone_instance
        mock_microphone_instance.__enter__.return_value = mock_microphone_instance  # Mock context manager

        # Mock the adjust_for_ambient_noise method
        mock_recognizer = MagicMock()
        mock_recognizer.adjust_for_ambient_noise = MagicMock()

        # Initialize the ConfigManager with the mock view and mocked recognizer
        mock_view = MagicMock()
        mock_view.ui = MagicMock()
        mock_view.state_machine = MagicMock()
        config_manager = ConfigManager(mock_view)
        config_manager.recognize = mock_recognizer

        # Call the method to test
        active_mics = config_manager.get_active_mics()

        # Ensure the microphone list is returned and parsed correctly
        self.assertEqual(active_mics, [[0, 'Mic 1'], [1, 'Mic 2'], [2, 'Mic 3']])
        mock_list_microphone_names.assert_called()
        mock_microphone.assert_called()

    @patch('speech_recognition.Microphone.list_microphone_names')
    @patch('speech_recognition.Microphone')
    def test_get_active_mics_waittimeout(self, mock_microphone, mock_list_microphone_names):
        # Test handling of sr.WaitTimeoutError (inactive mic)
        mock_list_microphone_names.return_value = ['Mic 1', 'Mic 2', 'Mic 3']

        # Mock the `Microphone` instance behavior
        mock_microphone_instance = MagicMock()
        mock_microphone.return_value = mock_microphone_instance
        mock_microphone_instance.__enter__.side_effect = sr.WaitTimeoutError  # Simulate timeout error

        # Mock the adjust_for_ambient_noise method
        mock_recognizer = MagicMock()
        mock_recognizer.adjust_for_ambient_noise = MagicMock()

        # Initialize the ConfigManager with the mock view and mocked recognizer
        mock_view = MagicMock()
        mock_view.ui = MagicMock()
        mock_view.state_machine = MagicMock()
        config_manager = ConfigManager(mock_view)
        config_manager.recognize = mock_recognizer

        # Call the method to test
        active_mics = config_manager.get_active_mics()

        # Assert that the mic is reported as inactive
        self.assertEqual(active_mics, [])
        mock_list_microphone_names.assert_called()

    @patch('speech_recognition.Microphone.list_microphone_names')
    @patch('speech_recognition.Microphone')
    def test_get_active_mics_exception(self, mock_microphone, mock_list_microphone_names):
        # Test handling of general exception (e.g., device failure)
        mock_list_microphone_names.return_value = ['Mic 1', 'Mic 2', 'Mic 3']

        # Mock the `Microphone` instance behavior
        mock_microphone_instance = MagicMock()
        mock_microphone.return_value = mock_microphone_instance
        mock_microphone_instance.__enter__.side_effect = Exception("Simulated error")  # Simulate general exception

        # Mock the adjust_for_ambient_noise method
        mock_recognizer = MagicMock()
        mock_recognizer.adjust_for_ambient_noise = MagicMock()

        # Initialize the ConfigManager with the mock view and mocked recognizer
        mock_view = MagicMock()
        mock_view.ui = MagicMock()
        mock_view.state_machine = MagicMock()
        config_manager = ConfigManager(mock_view)
        config_manager.recognize = mock_recognizer

        # Call the method to test
        active_mics = config_manager.get_active_mics()

        # Assert that the mic is reported with an error message (should be handled without crashing)
        self.assertEqual(active_mics, [])
        mock_list_microphone_names.assert_called()

    @patch('frontend.config_manager.ConfigManager.get_active_mics', return_value=[[1, 'Mic 1'], [7, 'Mic 7']])
    def test_get_first_active_mic_id(self, _):
        # Setup mock for get_active_mics to return the mocked list
        mock_view = MagicMock()
        mock_view.ui = MagicMock()
        mock_view.state_machine = MagicMock()
        config_manager = ConfigManager(mock_view)
        
        # Directly use the mocked active mics
        config_manager.active_mics = [[1, 'Mic 1'], [7, 'Mic 7']]

        # Call the method to test
        first_mic_id = config_manager.get_first_active_mic_id()

        # Ensure it returns the ID of the first active mic
        self.assertEqual(first_mic_id, 1)  # ID of the first active mic

        # Test the case where no active mics are present
        config_manager.active_mics = []
        first_mic_id_default = config_manager.get_first_active_mic_id()
        self.assertEqual(first_mic_id_default, 0)  # Default to 0 when no active mics are found

    @patch('frontend.config_manager.ConfigManager.get_active_mics', return_value=[[1, 'Mic 1'], [7, 'Mic 7']])
    def test_on_cb_select_mic_changed(self, _):
        # Test valid mic selection
        mock_view = MagicMock()
        mock_view.ui = MagicMock()
        mock_view.state_machine = MagicMock()
        config_manager = ConfigManager(mock_view)

        # Mock UI cb_select_mic
        mock_ui = MagicMock()
        config_manager.ui = mock_ui
        config_manager.ui.cb_select_mic.currentText.return_value = '1: Mic 1'  # Mock selected text

        # Mock the update_preference method
        config_manager.update_preference = MagicMock()

        # Call the method to test
        config_manager.on_cb_select_mic_changed(0)

        # Ensure the update_preference method is called with the correct mic ID
        config_manager.update_preference.assert_called_once_with('mic_id', 1)

        # Test invalid mic selection (malformed text)
        mock_ui.cb_select_mic.currentText.return_value = 'Invalid Mic Selection'  # Invalid format
        config_manager.on_cb_select_mic_changed(0)
        config_manager.update_preference.assert_called_once()  # Should not be called for invalid selection
        
        # Test empty selection (edge case)
        mock_ui.cb_select_mic.currentText.return_value = ''
        config_manager.on_cb_select_mic_changed(0)
        config_manager.update_preference.assert_called_once()  # Should not be called for empty text

    @patch('frontend.config_manager.ConfigManager.get_active_mics', return_value=[[1, 'Mic 1'], [7, 'Mic 7']])
    def test_on_cb_select_mic_changed_valid(self, _):
        """Test valid mic selection."""
        # Mock view and UI
        mock_view = MagicMock()
        mock_view.ui = MagicMock()
        mock_view.state_machine = MagicMock()
        config_manager = ConfigManager(mock_view)

        # Mock UI cb_select_mic
        mock_ui = MagicMock()
        config_manager.ui = mock_ui
        config_manager.ui.cb_select_mic.currentText.return_value = '1: Mic 1'  # Mock selected text

        # Mock the update_preference method
        config_manager.update_preference = MagicMock()

        # Call the method to test
        config_manager.on_cb_select_mic_changed(0)

        # Ensure the update_preference method is called with the correct mic ID
        config_manager.update_preference.assert_called_once_with('mic_id', 1)

    @patch('frontend.config_manager.ConfigManager.get_active_mics', return_value=[[1, 'Mic 1'], [7, 'Mic 7']])
    def test_on_cb_select_mic_changed_invalid_format(self, _):
        """Test invalid mic selection (malformed text)."""
        # Mock view and UI
        mock_view = MagicMock()
        mock_view.ui = MagicMock()
        mock_view.state_machine = MagicMock()
        config_manager = ConfigManager(mock_view)

        # Mock UI cb_select_mic
        mock_ui = MagicMock()
        config_manager.ui = mock_ui
        mock_ui.cb_select_mic.currentText.return_value = 'Invalid Mic Selection'  # Invalid format

        # Mock the update_preference method
        config_manager.update_preference = MagicMock()

        # Call the method to test
        config_manager.on_cb_select_mic_changed(0)

        # Ensure the update_preference method is NOT called for invalid selection
        config_manager.update_preference.assert_not_called()

    @patch('frontend.config_manager.ConfigManager.get_active_mics', return_value=[[1, 'Mic 1'], [7, 'Mic 7']])
    def test_on_cb_select_mic_changed_empty_selection(self, _):
        """Test empty selection (edge case)."""
        # Mock view and UI
        mock_view = MagicMock()
        mock_view.ui = MagicMock()
        mock_view.state_machine = MagicMock()
        config_manager = ConfigManager(mock_view)

        # Mock UI cb_select_mic
        mock_ui = MagicMock()
        config_manager.ui = mock_ui
        mock_ui.cb_select_mic.currentText.return_value = ''  # Empty selection

        # Mock the update_preference method
        config_manager.update_preference = MagicMock()

        # Call the method to test
        config_manager.on_cb_select_mic_changed(0)

        # Ensure the update_preference method is NOT called for empty selection
        config_manager.update_preference.assert_not_called()

    @patch('frontend.config_manager.ConfigManager.get_active_mics', return_value=[[1, 'Mic 1'], [7, 'Mic 7']])
    def test_on_cb_select_mic_changed_value_error(self, _):
        """Test ValueError exception in case of malformed microphone ID (non-integer value before colon)."""
        # Mock view and UI
        mock_view = MagicMock()
        mock_view.ui = MagicMock()
        mock_view.state_machine = MagicMock()
        config_manager = ConfigManager(mock_view)

        # Mock UI cb_select_mic
        mock_ui = MagicMock()
        config_manager.ui = mock_ui
        mock_ui.cb_select_mic.currentText.return_value = 'abc: Mic 1'  # Non-integer value before colon

        # Mock the update_preference method
        config_manager.update_preference = MagicMock()

        # Call the method to test
        config_manager.on_cb_select_mic_changed(0)

        # Ensure the update_preference method is NOT called due to ValueError
        config_manager.update_preference.assert_not_called()
