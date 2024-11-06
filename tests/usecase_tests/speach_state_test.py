import unittest
from unittest.mock import MagicMock
from usecases.speach_state import SpeachState

class TestSpeachState(unittest.TestCase):

    def setUp(self):
        self.state_machine = MagicMock()
        self.speach_state = SpeachState(self.state_machine)
        self.speach_state.stop = MagicMock()  # Mock the stop method
        self.speach_state.state_machine.goto_welcome = MagicMock()
        self.speach_state.state_machine.goto_welcome.on_enter = MagicMock()

    def test_on_enter(self):
        self.speach_state.voice_interface.speak = MagicMock()
        self.speach_state.voice_interface.listen = MagicMock(return_value="welcome")
        self.speach_state.check_triggers = MagicMock()

        self.speach_state.on_enter()
        self.speach_state.stop()  # Stop the loop

        self.speach_state.voice_interface.speak.assert_called()
        self.speach_state.check_triggers.assert_called()

    def test_check_triggers(self):
        self.speach_state.voice_interface.listen = MagicMock(return_value="welcome")
        self.speach_state.voice_interface.speak = MagicMock()
        self.speach_state.state_machine.goto_welcome = MagicMock()

        self.speach_state.check_triggers()

        self.speach_state.voice_interface.speak.assert_called_with("Wechsel zu Willkommensnachricht.")
        self.speach_state.state_machine.goto_welcome.assert_called()
        self.speach_state.state_machine.goto_welcome.on_enter.assert_not_called()