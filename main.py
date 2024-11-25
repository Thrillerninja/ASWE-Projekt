import sys
import threading
from loguru import logger
from PyQt5 import QtWidgets
from frontend.main_window import MainWindow
from usecases.state_machine import StateMachine

# Start the backend & state machine
sm = StateMachine()

# Function to run the state machine
def run_state_machine():
    logger.info("Starting state machine")
    sm.to_idle()
# Function to run the state machine
def run_state_machine():
    logger.info("Starting state machine")
    sm.to_idle()

# Start the state machine in a separate thread
state_machine_thread = threading.Thread(target=run_state_machine)
state_machine_thread.start()

# Start the UI
app = QtWidgets.QApplication(sys.argv)
window = MainWindow(sm)
window.show()

# Bring the window to the foreground
window.raise_()
window.activateWindow()

# Connect the aboutToQuit signal to the stop method
app.aboutToQuit.connect(sm.stop)

logger.info("Starting UI")
sys.exit(app.exec_())
