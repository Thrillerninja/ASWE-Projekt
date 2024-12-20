import unittest
from unittest.mock import patch, MagicMock
from PyQt5.QtWidgets import QApplication, QPushButton
from PyQt5.QtCore import QTime, QSize, QEvent
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'frontend')))
from frontend.main_window import MainWindow


app = QApplication(sys.argv)

class TestMainWindow(unittest.TestCase):
    def setUp(self):
        patcher_ui = patch('frontend.ui_templates.main_window.Ui_MainWindow', autospec=True)
        patcher_config = patch('frontend.config_manager.ConfigManager', autospec=True)
        patcher_get_active_mics = patch('frontend.config_manager.ConfigManager.get_active_mics', return_value=[[1, 'Mic 1'], [7, 'Mic 7']])
        
        patcher_get_active_mics.start()
        self.MockUi_MainWindow = patcher_ui.start()
        self.MockConfigManager = patcher_config.start()
        patch('frontend.main_window.logger.warning').start()

        self.addCleanup(patcher_ui.stop)
        self.addCleanup(patcher_config.stop)

        self.state_machine = MagicMock()
        self.main_window = MainWindow(self.state_machine)

        self.mock_ui = self.main_window.ui
        self.mock_config = self.main_window.config_manager

        self.mock_ui.lb_select_fuel_type = MagicMock()
        self.mock_ui.lb_select_fuel_threshold = MagicMock()
        self.mock_ui.lb_default_alarm_time = MagicMock()
        self.mock_ui.lb_sleep_time = MagicMock()
        self.mock_ui.cb_fuel_type = MagicMock()
        self.mock_ui.le_fuel_threshold = MagicMock()
        self.mock_ui.sl_fuel_threshold = MagicMock()
        self.mock_ui.te_default_alarm_time = MagicMock()
        self.mock_ui.te_sleep_time = MagicMock()
        self.mock_ui.bt_save_settings = MagicMock()
        self.mock_ui.bt_settings = MagicMock(spec=QPushButton)
        self.mock_ui.bt_speech_to_text = MagicMock(spec=QPushButton)
        self.mock_ui.lb_alarm = MagicMock()
        self.mock_ui.lb_alarm_text = MagicMock()
        self.mock_ui.lb_sound_wave_gif = MagicMock()
        self.mock_ui.lb_fuel_demo_price = MagicMock()
        self.mock_ui.le_fuel_demo_price = MagicMock()
        self.mock_ui.lb_select_mic = MagicMock()
        self.mock_ui.cb_select_mic = MagicMock()

        for el in self.mock_ui.__dict__.values():
            if isinstance(el, MagicMock):
                el.setVisible = MagicMock()

        self.mock_config.save_preferences = MagicMock()
        self.mock_movie = MagicMock()
        self.main_window.movie = self.mock_movie
        self.mock_ui.lb_sound_wave_gif = MagicMock()

        self.mock_style = MagicMock()
        self.mock_ui.le_fuel_threshold.style.return_value = self.mock_style

        self.settings_elements = [
            self.mock_ui.lb_select_fuel_type,
            self.mock_ui.lb_select_fuel_threshold,
            self.mock_ui.lb_default_alarm_time,
            self.mock_ui.lb_sleep_time,
            self.mock_ui.cb_fuel_type,
            self.mock_ui.le_fuel_threshold,
            self.mock_ui.sl_fuel_threshold,
            self.mock_ui.te_default_alarm_time,
            self.mock_ui.te_sleep_time,
            self.mock_ui.bt_save_settings,
            self.mock_ui.lb_fuel_demo_price,
            self.mock_ui.le_fuel_demo_price,
            self.mock_ui.lb_select_mic,
            self.mock_ui.cb_select_mic
        ]

        self.not_settings_elements = [
            self.mock_ui.bt_settings,
            self.mock_ui.bt_speech_to_text,
            self.mock_ui.lb_alarm,
            self.mock_ui.lb_alarm_text
        ]

        self.mock_ui.cb_fuel_type.count.return_value = 3
        self.mock_ui.sl_fuel_threshold.minimum.return_value = 0
        self.mock_ui.sl_fuel_threshold.maximum.return_value = 100
        self.mock_event = MagicMock()


    def test_toggle_view(self):
        """Test toggle_view switches the visibility of settings elements."""
        self.main_window.settings_are_hidden = True
        self.main_window.toggle_view()

        for el in self.settings_elements:
            el.setVisible.assert_called_with(False)

        for el in self.not_settings_elements:
            el.setVisible.assert_called_with(True)

    def test_on_bt_save_settings_clicked_no_error(self):
        """Test on_bt_save_settings_clicked saves preferences and toggles view when no error.""" 
        self.main_window.on_bt_save_settings_clicked()
        self.mock_config.save_preferences.assert_called_once()
        self.assertTrue(self.main_window.settings_are_hidden)

    def test_on_bt_save_settings_clicked_with_error(self):
        """Test on_bt_save_settings_clicked does not save preferences or toggle view when there's an error."""
        self.main_window.error_fuel_threshold = True
        self.main_window.error_fuel_demo_price = False

        self.main_window.on_bt_save_settings_clicked()
        self.mock_config.save_preferences.assert_not_called()
        self.assertFalse(self.main_window.settings_are_hidden)


    @patch('PyQt5.QtCore.QTimer.singleShot')
    def test_on_bt_speech_to_text_clicked(self, mock_single_shot):
        """Test on_bt_speech_to_text_clicked shows GIF, starts movie, and schedules stop recording."""
        self.main_window.on_bt_speech_to_text_clicked()
        self.mock_ui.lb_sound_wave_gif.setVisible.assert_called_with(True)
        self.mock_movie.start.assert_called_once()
        mock_single_shot.assert_called_once_with(3000, self.main_window.stop_recording)


    def test_stop_recording(self):
        """Test stop_recording stops the movie and hides GIF."""
        self.main_window.stop_recording()

        self.mock_ui.lb_sound_wave_gif.setVisible.assert_called_with(False)
        self.main_window.movie.stop.assert_called_once()

    def test_show_error_le_fuel_threshold(self):
        """Test show_error_le_fuel_threshold sets error properties correctly."""
        error_message = "Fuel threshold must be a number between 1.00 and 2.00"

        self.main_window.show_error_le_fuel_threshold(error_message)

        self.mock_ui.le_fuel_threshold.setProperty.assert_called_with("class", "error")

        self.mock_ui.le_fuel_threshold.style().unpolish.assert_called_with(self.mock_ui.le_fuel_threshold)
        self.mock_ui.le_fuel_threshold.style().polish.assert_called_with(self.mock_ui.le_fuel_threshold)

        self.mock_ui.le_fuel_threshold.setToolTip.assert_called_with(error_message)

    def test_remove_error_le_fuel_threshold(self):
        """Test remove_error_le_fuel_threshold removes error properties correctly."""
        self.main_window.remove_error_le_fuel_threshold()
        self.mock_ui.le_fuel_threshold.setProperty.assert_called_with("class", "")

        self.mock_ui.le_fuel_threshold.style().unpolish.assert_called_with(self.mock_ui.le_fuel_threshold)
        self.mock_ui.le_fuel_threshold.style().polish.assert_called_with(self.mock_ui.le_fuel_threshold)

    def test_show_error_le_fuel_demo_price(self):
        """Test show_error_le_fuel_demo_price sets error properties correctly."""
        error_message = "Fuel threshold must be a number between 1.00 and 2.00"

        self.main_window.show_error_le_fuel_demo_price(error_message)

        self.mock_ui.le_fuel_demo_price.setProperty.assert_called_with("class", "error")

        self.mock_ui.le_fuel_demo_price.style().unpolish.assert_called_with(self.mock_ui.le_fuel_demo_price)
        self.mock_ui.le_fuel_demo_price.style().polish.assert_called_with(self.mock_ui.le_fuel_demo_price)

        self.mock_ui.le_fuel_demo_price.setToolTip.assert_called_with(error_message)

    def test_remove_error_le_fuel_demo_price(self):
        """Test remove_error_le_fuel_demo_price removes error properties correctly."""
        self.main_window.remove_error_le_fuel_demo_price()
        self.mock_ui.le_fuel_demo_price.setProperty.assert_called_with("class", "")

        self.mock_ui.le_fuel_demo_price.style().unpolish.assert_called_with(self.mock_ui.le_fuel_demo_price)
        self.mock_ui.le_fuel_demo_price.style().polish.assert_called_with(self.mock_ui.le_fuel_demo_price)

    @patch("builtins.print")
    def test_set_cb_fuel_type_valid(self, mock_print):
        """Test that set_cb_fuel_type sets the current index when the value is valid."""
        self.main_window.set_cb_fuel_type(1)
        self.mock_ui.cb_fuel_type.setCurrentIndex.assert_called_with(1)
        mock_print.assert_not_called()

    @patch("builtins.print")
    def test_set_cb_fuel_type_invalid(self, mock_print):
        """Test that set_cb_fuel_type prints a message when the value is out of range."""
        self.main_window.set_cb_fuel_type(5)
        self.mock_ui.cb_fuel_type.setCurrentIndex.assert_not_called()
        mock_print.assert_called_with("Value 5 is out of range for fuel type selection.")

    def test_set_te_default_alarm_time(self):
        """Test that set_te_default_alarm_time sets the time correctly."""
        test_time = QTime(8, 30)
        self.main_window.set_te_default_alarm_time(test_time)
        self.mock_ui.te_default_alarm_time.setTime.assert_called_with(test_time)

    def test_set_te_sleep_time(self):
        """Test that set_te_sleep_time sets the time correctly."""
        test_time = QTime(22, 0)
        self.main_window.set_te_sleep_time(test_time)
        self.mock_ui.te_sleep_time.setTime.assert_called_with(test_time)

    def test_set_sl_fuel_threshold_within_range(self):
        """Test that set_sl_fuel_threshold sets the value when it's within the range."""
        valid_value = 50
        self.main_window.set_sl_fuel_threshold(valid_value)
        self.mock_ui.sl_fuel_threshold.setValue.assert_called_with(valid_value)

    def test_set_sl_fuel_threshold_out_of_range(self):
        """Test that set_sl_fuel_threshold does not set the value if it's out of range."""
        invalid_value = 150
        with patch('builtins.print') as mocked_print:
            self.main_window.set_sl_fuel_threshold(invalid_value)
            self.mock_ui.sl_fuel_threshold.setValue.assert_not_called()
            mocked_print.assert_called_with(f"Value {invalid_value} is out of range for the fuel threshold slider.")

    def test_set_le_fuel_threshold(self):
        """Test that set_le_fuel_threshold correctly sets the text with currency symbol."""
        text_value = "1.53"
        self.main_window.set_le_fuel_threshold(text_value)
        self.mock_ui.le_fuel_threshold.setText.assert_called_with(f'{text_value} €')

    def test_set_le_fuel_threshold_with_integer(self):
        """Test that set_le_fuel_threshold correctly handles integer input."""
        text_value = "50"
        self.main_window.set_le_fuel_threshold(text_value)
        self.mock_ui.le_fuel_threshold.setText.assert_called_with(f'{text_value} €')

    def test_set_le_fuel_threshold_with_invalid_input(self):
        """Test that set_le_fuel_threshold handles unexpected input gracefully."""
        text_value = "invalid_input"
        self.main_window.set_le_fuel_threshold(text_value)
        self.mock_ui.le_fuel_threshold.setText.assert_called_with(f'{text_value} €')

    def test_set_le_fuel_demo_price(self):
        """Test that set_le_fuel_demo_price correctly sets the text with currency symbol."""
        text_value = "1.53"
        self.main_window.set_le_fuel_demo_price(text_value)
        self.mock_ui.le_fuel_demo_price.setText.assert_called_with(f'{text_value} €')

    def test_set_le_fuel_demo_price_with_integer(self):
        """Test that set_le_fuel_demo_price correctly handles integer input."""
        text_value = "50"
        self.main_window.set_le_fuel_demo_price(text_value)
        self.mock_ui.le_fuel_demo_price.setText.assert_called_with(f'{text_value} €')

    def test_set_le_fuel_demo_price_with_invalid_input(self):
        """Test that set_le_fuel_demo_price handles unexpected input gracefully."""
        text_value = "invalid_input"
        self.main_window.set_le_fuel_demo_price(text_value)
        self.mock_ui.le_fuel_demo_price.setText.assert_called_with(f'{text_value} €')

    def test_set_alarm(self):
        """Test that set_alarm correctly sets the alarm text."""
        alarm_time = "08:00"
        self.main_window.set_alarm(alarm_time)
        self.mock_ui.lb_alarm_text.setText.assert_called_with(alarm_time)

    def test_set_alarm_with_different_time(self):
        """Test that set_alarm correctly sets a different alarm time."""
        alarm_time = "16:30"
        self.main_window.set_alarm(alarm_time)
        self.mock_ui.lb_alarm_text.setText.assert_called_with(alarm_time)

    def test_set_alarm_with_empty_time(self):
        """Test that set_alarm correctly handles an empty alarm time."""
        alarm_time = ""
        self.main_window.set_alarm(alarm_time)
        self.mock_ui.lb_alarm_text.setText.assert_called_with(alarm_time)

    @patch('PyQt5.QtWidgets.QApplication.quit')
    def test_closeEvent(self, mock_quit):
        """Test that closeEvent calls save_preferences and quits the application."""
        self.mock_config.save_preferences = MagicMock()
        self.main_window.closeEvent(self.mock_event)
        self.mock_config.save_preferences.assert_called_once()
        mock_quit.assert_called_once()

    def test_on_hover_enter_settings(self):
        """Test that the icon size of the settings button changes when hovering enters."""
        self.mock_ui.bt_settings.size.return_value = QSize(40, 40)
        mock_event = MagicMock()

        self.main_window.on_hover_enter_settings(mock_event)

        expected_size = QSize(36, 36)  # 36 is 90% of original size (40)
        self.mock_ui.bt_settings.setIconSize.assert_called_once_with(expected_size)

    def test_on_hover_leave_settings(self):
        """Test that the icon size of the settings button changes when hovering leaves."""
        self.mock_ui.bt_settings.size.return_value = QSize(40, 40)
        mock_event = MagicMock()

        self.main_window.on_hover_leave_settings(mock_event)

        expected_size = QSize(32, 32)  # 32 is 80% of original size (40)
        self.mock_ui.bt_settings.setIconSize.assert_called_once_with(expected_size)

    def test_on_hover_enter_speech_to_text(self):
        """Test that the icon size of the speech-to-text button changes when hovering enters."""
        mock_event = MagicMock()
        self.main_window.on_hover_enter_speech_to_text(mock_event)

        expected_size = QSize(38, 38)
        self.mock_ui.bt_speech_to_text.setIconSize.assert_called_once_with(expected_size)

    def test_on_hover_leave_speech_to_text(self):
        """Test that the icon size of the speech-to-text button changes when hovering leaves."""
        mock_event = MagicMock()
        self.main_window.on_hover_leave_speech_to_text(mock_event)

        expected_size = QSize(35, 35)
        self.mock_ui.bt_speech_to_text.setIconSize.assert_called_once_with(expected_size)

    @patch('frontend.main_window.logger.warning')
    def test_set_mic_id_correct_id(self, mock_warning):
        # Test that set_mic_id correctly sets the microphone
        self.main_window.set_mic_id(1)  # Select "Mic 1"
        
        # Ensure the combobox index is set to the correct item
        self.mock_ui.cb_select_mic.setCurrentIndex.assert_called_once_with(0) # Mic 1 is the first item
        
        # Check that no warning was logged
        mock_warning.assert_not_called()

    @patch('frontend.main_window.logger.warning')
    def test_set_mic_id_id_not_found(self, mock_warning):
        # Test that if the mic_id is not found, a warning is logged
        self.main_window.set_mic_id(99)  # Non-existent mic_id
        
        # Ensure the combobox index is not changed
        self.mock_ui.cb_select_mic.setCurrentIndex.assert_not_called()
        
        # Check that a warning was logged
        mock_warning.assert_called_once_with("Microphone with ID 99 not found in combobox.")

    def test_set_mic_list(self):
        # Test that set_mic_list correctly sets the items in the combo box
        mic_list = [[1, "Mic 1"], [2, "Mic 2"], [7, "Mic 7"]]
        self.main_window.set_mic_list(mic_list)
        
        # Ensure the combo box is cleared and items are added in the correct format
        self.mock_ui.cb_select_mic.clear.assert_called_once()
        self.mock_ui.cb_select_mic.addItems.assert_called_once_with(["1: Mic 1", "2: Mic 2", "7: Mic 7"])

    def test_set_mic_list_empty(self):
        # Test that set_mic_list handles an empty list gracefully
        self.main_window.set_mic_list([])
        
        # Ensure the combo box is cleared
        self.mock_ui.cb_select_mic.clear.assert_called_once()
        # Ensure no items are added
        self.mock_ui.cb_select_mic.addItems.assert_not_called()
