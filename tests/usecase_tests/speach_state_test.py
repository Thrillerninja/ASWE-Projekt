import unittest
from unittest.mock import patch, MagicMock
from usecases.speach_state import SpeachState
from usecases.state_machine import StateMachine

class TestSpeachState(unittest.TestCase):

    @patch('usecases.speach_state.SpeachState.process_input')
    def test_on_enter(self, mock_process_input):
        state_machine = StateMachine()
        speach_state = SpeachState(state_machine)

        # Mock APIs
        speach_state.voice_interface = MagicMock()

        speach_state.on_enter()

        # Check if TTS API was called with the correct message
        speach_state.voice_interface.speak.assert_any_call("Bitte sprechen Sie einen Befehl.")
        speach_state.voice_interface.speak.assert_any_call("Spracherkennung beendet.")

    def test_check_triggers_idle(self):
        state_machine = StateMachine()
        state_machine.testing = True
        
        # Mock the API factory to avoid creating actual API instances
        state_machine.api_factory.create_api = MagicMock()

        # Mock voice interface
        state_machine.speach.voice_interface = MagicMock()
        state_machine.speach.testing = True

        # transition to speach state
        state_machine.interact()
        
        state_machine.speach.voice_interface.listen.voice_interface = MagicMock()

        # Mock the listen method to return "beenden"
        state_machine.speach.voice_interface.listen.return_value = "beenden"

        # Test check_triggers method
        state_machine.speach.check_triggers()

        # Check if the correct message was spoken and the state transition to idle was triggered
        state_machine.speach.voice_interface.speak.assert_called_with("Spracherkennung wird beendet.")
        
    def test_check_triggers_welcome(self):
        state_machine = StateMachine()
        state_machine.testing = True
        
        # Mock the API factory to avoid creating actual API instances
        state_machine.api_factory.create_api = MagicMock()

        # Mock voice interface
        state_machine.speach.voice_interface = MagicMock()
        state_machine.speach.testing = True
        
        state_machine.welcome.tts_api = MagicMock()
        state_machine.on_enter = MagicMock()

        # transition to speach state
        state_machine.interact()
        
        state_machine.speach.voice_interface.listen.voice_interface = MagicMock()

        # Mock the listen method to return "willkommen"
        state_machine.speach.voice_interface.listen.return_value = "willkommen"

        # Test check_triggers method
        state_machine.speach.check_triggers()
        
        # Check if the correct message was spoken and the state transition to welcome was triggered
        state_machine.speach.voice_interface.speak.assert_called_with("Wechsel zu Willkommensnachricht.")
        
    def test_check_triggers_finance(self):
        state_machine = StateMachine()
        state_machine.testing = True
        
        # Mock the API factory to avoid creating actual API instances
        state_machine.api_factory.create_api = MagicMock()

        # Mock voice interface
        state_machine.speach.voice_interface = MagicMock()
        state_machine.speach.testing = True
        
        state_machine.on_enter = MagicMock()

        # transition to speach state
        state_machine.interact()
        
        state_machine.speach.voice_interface.listen.voice_interface = MagicMock()

        # Mock the listen method to return "willkommen"
        state_machine.speach.voice_interface.listen.return_value = "finanzen"

        # Test check_triggers method
        state_machine.speach.check_triggers()
        
        # Check if the correct message was spoken and the state transition to welcome was triggered
        state_machine.speach.voice_interface.speak.assert_called_with("Wechsel zu Finanzinformationen.")