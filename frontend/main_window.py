import sys
from PyQt5 import QtWidgets

from ui_templates.main_window import Ui_MainWindow
from config_manager import ConfigManager


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.config_manager = ConfigManager(self)
        self.ui.setupUi(self)

        self.value_map = {
            'Super E10': 'super-e10',
            'Super E5': 'super-e5',
            'Super Plus': 'super-plus',
            'Diesel': 'diesel',
            'LKW Diesel': 'lkw-diesel',
            'LPG': 'lpg',
        }

        self.reverse_value_map = {v: k for k, v in self.value_map.items()}
        self.load_initial_fuel_type()

        self.ui.bt_exit.clicked.connect(self.on_bt_exit_clicked)
        self.ui.cb_fuel_type.currentTextChanged.connect(self.on_fuel_type_changed)

    def on_bt_exit_clicked(self):
        pass

    def on_fuel_type_changed(self, selected_text):
        selected_data = self.value_map.get(selected_text, None)
        self.config_manager.set_fuel_type(selected_data)

    def load_initial_fuel_type(self):
        """Load the fuel type from preferences and set the combo box accordingly."""

        saved_fuel_type = self.config_manager.get_fuel_type()
        if saved_fuel_type:
            display_fuel_type = self.reverse_value_map.get(saved_fuel_type, None)
            self.ui.cb_fuel_type.setCurrentText(display_fuel_type)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
