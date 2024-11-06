import unittest
from unittest.mock import MagicMock, patch
from usecases.idle_state import IdleState

class TestIdleState(unittest.TestCase):
    def setUp(self):
        self.state_machine = MagicMock()
        self.idle_state = IdleState(self.state_machine)

    @patch('usecases.idle_state.IdleState.check_triggers')
    def test_on_enter(self, mock_check_triggers):
        # Prevent infinite loop by allowing check_triggers to run only once
        self.idle_state._running = True
        self.idle_state._test_break_loop = True  # Set the test flag to break the loop

        # Call on_enter to test if check_triggers is invoked once
        self.idle_state.on_enter()
        
        # Assert check_triggers was called exactly once
        mock_check_triggers.assert_called_once()

    def test_check_triggers(self):
        # Setup the start method on the state machine to ensure it's called
        self.state_machine.start = MagicMock()

        # Call check_triggers to see if it triggers start
        self.idle_state.check_triggers()

        # Assert start was called exactly once on the state machine
        self.state_machine.start.assert_called_once()

    def test_stop(self):
        # Test if stop correctly sets _running to False
        self.idle_state.stop()
        self.assertFalse(self.idle_state._running)

if __name__ == '__main__':
    unittest.main()
