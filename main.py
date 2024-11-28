import sys
# from PyQt5 import QtWidgets
# from frontend.main_window import MainWindow
from usecases.state_machine import StateMachine

# Start the backend & state machine
sm = StateMachine()

# Transition to initial state
sm.to_idle()

# Start the UI
# app = QtWidgets.QApplication(sys.argv)
# window = MainWindow(sm)
# window.show()
#sys.exit(app.exec_())
