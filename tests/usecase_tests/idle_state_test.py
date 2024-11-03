import unittest
from unittest.mock import MagicMock
from usecases.idle_state import IdleState

class TestIdleState(unittest.TestCase):

    def setUp(self):
        self.state_machine = MagicMock()
        self.idle_state = IdleState(self.state_machine)

    def test_on_enter(self):
        self.idle_state.check_triggers = MagicMock()
        self.idle_state.on_enter()
        self.idle_state.check_triggers.assert_called()

    def test_check_triggers(self):
        self.idle_state.check_triggers()
        self.state_machine.start.assert_called()