import unittest
from unittest.mock import MagicMock
from usecases.state_machine import StateMachine

class TestStateMachine(unittest.TestCase):

    def setUp(self):
        self.state_machine = StateMachine()

    def test_initial_state(self):
        self.assertEqual(self.state_machine.state, 'idle')

    def test_transition_to_welcome(self):
        self.state_machine.start()
        self.assertEqual(self.state_machine.state, 'welcome')

    def test_transition_to_speach(self):
        self.state_machine.interact()
        self.assertEqual(self.state_machine.state, 'speach')

    def test_transition_to_news(self):
        self.state_machine.start()
        self.state_machine.morning_news()
        self.assertEqual(self.state_machine.state, 'news')

    def test_transition_to_finance(self):
        self.state_machine.interact()
        self.state_machine.goto_finance()
        self.assertEqual(self.state_machine.state, 'finance')

    def test_transition_to_activity(self):
        self.state_machine.interact()
        self.state_machine.goto_activity()
        self.assertEqual(self.state_machine.state, 'activity')

    def test_transition_back_to_idle(self):
        self.state_machine.start()
        self.state_machine.exit()
        self.assertEqual(self.state_machine.state, 'idle')
