import unittest
from unittest.mock import patch, MagicMock
from usecases.state_machine import StateMachine

class TestStateMachine(unittest.TestCase):

    @patch('usecases.welcome_state.WelcomeState.on_enter')
    @patch('usecases.speach_state.SpeachState.on_enter')
    def test_state_transitions(self, mock_speach_on_enter, mock_welcome_on_enter):
        state_machine = StateMachine()
        state_machine.testing = True

        # Test transition from idle to welcome
        state_machine.start()
        self.assertEqual(state_machine.state, 'welcome')
        mock_welcome_on_enter.assert_called_once()

        # Test transition from welcome to speach
        state_machine.interaction()
        self.assertEqual(state_machine.state, 'speach')
        mock_speach_on_enter.assert_called_once()

        # Test transition from speach to idle
        state_machine.goto_idle()
        self.assertEqual(state_machine.state, 'idle')

if __name__ == '__main__':
    unittest.main()
