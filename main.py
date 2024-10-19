import sys
from PyQt5 import QtWidgets
from frontend.main_window import MainWindow
from usecases.state_machine import StateMachine

# Start the UI
#app = QtWidgets.QApplication(sys.argv)
#window = MainWindow()
#window.show()
# Start the backand & state machine
sm = StateMachine()
#sys.exit(app.exec_())

