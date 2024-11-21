import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTime, QTimer
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtGui import QMovie

from frontend.ui_templates.main_window import Ui_MainWindow
from frontend.config_manager import ConfigManager
from usecases.state_machine import StateMachine

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, state_machine: StateMachine):
        self.state_machine = state_machine
        
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.config_manager = ConfigManager(self)

        self.movie = QMovie("frontend/ui_templates/sound_wave.gif")
        self.ui.lb_sound_wave_gif.setMovie(self.movie)
        self.ui.lb_sound_wave_gif.setVisible(False)

        self.settings_are_hidden = True
        self.toggle_view()

        self.ui.bt_settings.clicked.connect(self.toggle_view)
        self.ui.bt_save_settings.clicked.connect(self.on_bt_save_settings_clicked)
        self.ui.bt_speech_to_text.clicked.connect(self.on_bt_speech_to_text_clicked)

        self.ui.cb_fuel_type.currentIndexChanged.connect(self.config_manager.on_cb_fuel_type_changed)

        self.ui.te_default_alarm_time.timeChanged.connect(
            lambda time: self.config_manager.on_time_changed("default_alarm_time", time)
        )

        self.ui.te_sleep_time.timeChanged.connect(
            lambda time: self.config_manager.on_time_changed("sleep_time", time)
        )

        self.ui.sl_fuel_threshold.valueChanged.connect(self.config_manager.on_sl_fuel_threshold_changed)
        self.ui.le_fuel_threshold.editingFinished.connect(
            lambda: self.config_manager.on_le_fuel_threshold_changed(self.ui.le_fuel_threshold.text())
        )

        self.ui.le_fuel_demo_price.editingFinished.connect(
            lambda: self.config_manager.on_le_fuel_demo_price_changed(self.ui.le_fuel_demo_price.text())
        )

        self.error_fuel_threshold = False
        self.error_fuel_demo_price = False

    def on_bt_save_settings_clicked(self) -> None:
        """Saves preferences and toggles the view.

        This method saves the current settings and switches the UI view between settings and non-settings.
        """
        if self.error_fuel_threshold or self.error_fuel_demo_price:
            return
        
        self.config_manager.save_preferences()
        self.toggle_view()

    def on_bt_speech_to_text_clicked(self) -> None:
        """Handler for button click event to start showing the GIF."""
        self.ui.lb_sound_wave_gif.setVisible(True)
        self.movie.start() 
        QTimer.singleShot(3000, self.stop_recording)  #TODO Implement speech to text

    def stop_recording(self) -> None:
        """Stop the recording and hide the GIF."""
        self.ui.lb_sound_wave_gif.setVisible(False)
        self.movie.stop()

    def closeEvent(self, event) -> None:
        """Override the closeEvent method to close the application gracefully, 
        saving preferences and quitting."""
        self.config_manager.save_preferences()
        QApplication.quit()

    def toggle_view(self) -> None:
        """Toggles visibility of settings and non-settings elements.

        Shows or hides the settings elements based on the `settings_are_hidden` flag.
        """
        settings_elements = [
            self.ui.lb_select_fuel_type,
            self.ui.lb_select_fuel_threshold,
            self.ui.lb_default_alarm_time,
            self.ui.lb_sleep_time,
            self.ui.cb_fuel_type,
            self.ui.le_fuel_threshold,
            self.ui.sl_fuel_threshold,
            self.ui.te_default_alarm_time,
            self.ui.te_sleep_time,
            self.ui.bt_save_settings,
            self.ui.lb_fuel_demo_price,
            self.ui.le_fuel_demo_price
        ]
        
        not_settings_elements = [
            self.ui.bt_settings,
            self.ui.bt_speech_to_text,
            self.ui.lb_alarm,
            self.ui.lb_alarm_text
        ]
        
        if self.settings_are_hidden:
            for el in settings_elements:
                el.setVisible(False)
            for el in not_settings_elements:
                el.setVisible(True)
        else:
            for el in settings_elements:
                el.setVisible(True)
            for el in not_settings_elements:
                el.setVisible(False)

        self.settings_are_hidden = not self.settings_are_hidden

    def show_error_le_fuel_threshold(self, message: str) -> None:
        """Displays an error message for the fuel threshold input field and shows a message box.

        Args:
            message (str): The error message to show.
        """
        self.error_fuel_threshold = True
        self.ui.le_fuel_threshold.setProperty("class", "error")
        self.ui.le_fuel_threshold.style().unpolish(self.ui.le_fuel_threshold)  # Re-apply the style
        self.ui.le_fuel_threshold.style().polish(self.ui.le_fuel_threshold)
        self.ui.le_fuel_threshold.setToolTip(message)

    def show_error_le_fuel_demo_price(self, message: str) -> None:
        """Displays an error message for the fuel demo price input field and shows a message box.

        Args:
            message (str): The error message to show.
        """
        self.error_fuel_demo_price = True
        self.ui.le_fuel_demo_price.setProperty("class", "error")
        self.ui.le_fuel_demo_price.style().unpolish(self.ui.le_fuel_demo_price)  # Re-apply the style
        self.ui.le_fuel_demo_price.style().polish(self.ui.le_fuel_demo_price)
        self.ui.le_fuel_demo_price.setToolTip(message)

    def remove_error_le_fuel_threshold(self) -> None:
        """Removes error indication from the fuel threshold input."""
        self.error_fuel_threshold = False
        self.ui.le_fuel_threshold.setProperty("class", "")
        self.ui.le_fuel_threshold.style().unpolish(self.ui.le_fuel_threshold)
        self.ui.le_fuel_threshold.style().polish(self.ui.le_fuel_threshold)

    def remove_error_le_fuel_demo_price(self) -> None:
        """Removes error indication from the fuel demo price input."""
        self.error_fuel_demo_price = False
        self.ui.le_fuel_demo_price.setProperty("class", "")
        self.ui.le_fuel_demo_price.style().unpolish(self.ui.le_fuel_demo_price)
        self.ui.le_fuel_demo_price.style().polish(self.ui.le_fuel_demo_price)

    def set_cb_fuel_type(self, value: int) -> None:
        """
        Sets the current index of the fuel type combo box.

        Args:
            value (int): The index of the fuel type to select in the combo box.
                         Should be within the range of available items.
        """
        if 0 <= value < self.ui.cb_fuel_type.count():
            self.ui.cb_fuel_type.setCurrentIndex(value)
        else:
            print(f"Value {value} is out of range for fuel type selection.")

    def set_te_default_alarm_time(self, time: QTime) -> None:
        """
        Sets the time in the default alarm time editor.

        Args:
            time (QTime): The time to set in the alarm time editor.
                          Must be a valid QTime object.
        """
        self.ui.te_default_alarm_time.setTime(time)

    def set_te_sleep_time(self, time: QTime) -> None:
        """
        Sets the time in the sleep time editor.

        Args:
            time (QTime): The time to set in the sleep time editor.
                          Must be a valid QTime object.
        """
        self.ui.te_sleep_time.setTime(time)

    def set_sl_fuel_threshold(self, value: int) -> None:
        """
        Sets the value of the fuel threshold slider.

        Args:
            value (int): The value to set on the slider, which should be
                         within the slider's range.
        """
        if self.ui.sl_fuel_threshold.minimum() <= value <= self.ui.sl_fuel_threshold.maximum():
            self.ui.sl_fuel_threshold.setValue(value)
        else:
            print(f"Value {value} is out of range for the fuel threshold slider.")

    def set_le_fuel_threshold(self, text: str) -> None:
        """
        Sets the text of the fuel threshold line edit.

        Args:
            text (str): The text to display in the line edit.
                        It should represent a float value as a string.
        """
        self.ui.le_fuel_threshold.setText(f'{text} €')

    def set_le_fuel_demo_price(self, text: str) -> None:
        """
        Sets the text of the fuel demo price line edit.

        Args:
            text (str): The text to display in the line edit.
                        It should represent a float value as a string.
        """
        self.ui.le_fuel_demo_price.setText(f'{text} €')

    def set_alarm(self, time: str):
        """
        Set the alarm text display with the specified time.

        Args:
            time (str): The alarm time to display in the alarm label.
        """
        self.ui.lb_alarm_text.setText(time)

# if __name__ == "__main__":
#     app = QtWidgets.QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec_())