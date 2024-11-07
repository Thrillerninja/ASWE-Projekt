import sys
from PyQt5 import QtWidgets
from .ui_templates.main_window import Ui_MainWindow
from usecases.state_machine import StateMachine

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, state_machine: StateMachine):
        self.state_machine = state_machine
        
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.bt_exit.clicked.connect(self.on_bt_exit_clicked)

    def on_bt_exit_clicked(self):
        pass
    
    # Prototype of voice activation button state change
    def on_bt_voice_clicked(self):
        self.state_machine.to_