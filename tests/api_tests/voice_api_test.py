import unittest
from unittest.mock import patch, MagicMock, mock_open
from api.tts_api import TTSAPI
import pyttsx3
import speech_recognition as sr
from config import CONFIG
import json
import pygame

class TestVoiceInterface(unittest.TestCase):
    def setUp(self):
        patch('api.tts_api.TTSAPI.get_elevenlabs_preference', return_value=False).start()

        self.api_key = CONFIG['elevenlabs_key']
        self.voice_interface = TTSAPI(self.api_key)
        self.voice_interface.engine = MagicMock()

    def tearDown(self):
        patch.stopall()

    @patch('pyttsx3.init')
    def test_init(self, mock_pyttsx3_init):
        """
        Test initialization of VoiceInterface
        """
        mock_pyttsx3_init.return_value = self.voice_interface.engine

        vi = TTSAPI(self.api_key)
        mock_pyttsx3_init.assert_called_once()
        self.assertIsNotNone(vi.r)

    @patch('pyttsx3.init')
    def test_speak(self, mock_pyttsx3_init):
        """
        Test speak functionality of the system with valid and invalid inputs
        """
        mock_engine = MagicMock()
        mock_pyttsx3_init.return_value = mock_engine

        vi = TTSAPI(self.api_key)
        vi.speak("Hello")
        mock_engine.say.assert_called_with("Hello")
        mock_engine.runAndWait.assert_called_once()

        # Test empty string
        with self.assertRaises(ValueError):
            vi.speak("")

        # Test non-string input
        with self.assertRaises(ValueError):
            vi.speak(123)

    @patch('speech_recognition.Recognizer.recognize_google')
    @patch('speech_recognition.Recognizer.listen')
    @patch('speech_recognition.Microphone')
    def test_listen_general_error(self, mock_microphone, mock_listen, mock_recognize_google):
        """
        Test listen handling for a general exception
        """
        mock_listen.return_value = MagicMock()
        mock_recognize_google.side_effect = Exception("General Error")

        result = self.voice_interface.listen()
        self.assertIn("Ein Fehler ist aufgetreten", result)
        
    @patch('api.tts_api.main.TTSAPI.listen')
    def test_yes_no(self, mock_listen):
        """
        Test ask_yes_no functionality
        """
        question = "Do you like ice cream?"
        with patch.object(self.voice_interface, 'speak') as mock_speak:
            # Test case where user responds with 'yes'
            mock_listen.return_value = "yes"
            self.assertTrue(self.voice_interface.ask_yes_no(question))
            mock_speak.assert_any_call(question)

            # Test case where user responds with 'no'
            mock_listen.return_value = "no"
            self.assertFalse(self.voice_interface.ask_yes_no(question))
            mock_speak.assert_any_call(question)

            # Test case where user responds with an unrecognized answer
            mock_listen.side_effect = ["I don't know", "yes"]
            self.assertTrue(self.voice_interface.ask_yes_no(question))
            mock_speak.assert_any_call(question)
            mock_speak.assert_any_call("Entschuldigung, ich habe Ihre Antwort nicht verstanden. Bitte antworten Sie mit ja oder nein.")

    @patch('speech_recognition.Microphone.list_microphone_names', return_value=['Microphone 1', 'Microphone 2'])
    def test_list_mics(self, mock_list_microphone_names):
        """Test the list_mics function to check available microphones."""

        # Call the list_mics method
        mics = self.voice_interface.list_mics()

        # Assert the mocked list of microphones was returned
        self.assertEqual(mics, ['Microphone 1', 'Microphone 2'])

        # Ensure the list_microphone_names function was called once
        mock_list_microphone_names.assert_called_once()

    @patch('speech_recognition.Microphone.list_microphone_names', return_value=[])
    def test_list_mics_no_mics(self, mock_list_microphone_names):
        """Test the list_mics function when no microphones are available."""

        # Call the list_mics method
        mics = self.voice_interface.list_mics()

        # Assert the list is empty when no mics are available
        self.assertEqual(mics, [])

        # Ensure the list_microphone_names function was called once
        mock_list_microphone_names.assert_called_once()

    @patch('speech_recognition.Microphone.list_microphone_names', return_value=['Mic 1', 'Mic 2', 'Mic 3'])
    @patch('builtins.print')  # Mock print to test that it was called
    def test_list_mics_prints_output(self, mock_print, mock_list_microphone_names):
        """Test that the list_mics function prints out the microphone names."""

        # Call the list_mics method
        self.voice_interface.list_mics()

        # Assert that the print function was called for each microphone
        mock_print.assert_any_call("Available microphones:")
        mock_print.assert_any_call("0: Mic 1")
        mock_print.assert_any_call("1: Mic 2")
        mock_print.assert_any_call("2: Mic 3")
        
        # Ensure the list_microphone_names function was called once
        mock_list_microphone_names.assert_called_once()

class TestGetElevenlabsPreference(unittest.TestCase):

    def setUp(self):
        """Set up the mocks and the instance of TTSAPI."""
        self.api_key = "mock_api_key"
        self.preferences_file = './config/preferences.json'

    @patch('builtins.open', new_callable=mock_open)
    def test_get_elevenlabs_preference_valid(self, mock_file):
        """Test when preferences.json exists and contains valid data."""
        # Simulate valid JSON content with 'enable_elevenlabs' set to 1 (True)
        mock_file.return_value.read.return_value = json.dumps({'enable_elevenlabs': 1})

        # Instantiate the TTSAPI class
        vi = TTSAPI(self.api_key)

        # Verify that the file was opened and read
        mock_file.assert_called_once_with(self.preferences_file, 'r')

        # Ensure that toggle_elevenlabs was set to True based on the valid JSON content
        self.assertTrue(vi.toggle_elevenlabs)

    @patch('builtins.open', new_callable=mock_open)
    def test_get_elevenlabs_preference_missing_enable_elevenlabs(self, mock_file):
        """Test when preferences.json exists but is missing the 'enable_elevenlabs' field."""
        # Simulate JSON without 'enable_elevenlabs' key (defaults to 0)
        mock_file.return_value.read.return_value = json.dumps({'other_field': 1})

        # Instantiate the TTSAPI class
        vi = TTSAPI(self.api_key)

        # Verify that the file was opened and read
        mock_file.assert_called_once_with(self.preferences_file, 'r')

        # Ensure that toggle_elevenlabs was set to False due to the absence of 'enable_elevenlabs'
        self.assertFalse(vi.toggle_elevenlabs)

    @patch('builtins.open', new_callable=mock_open)
    def test_get_elevenlabs_preference_file_not_found(self, mock_file):
        """Test when preferences.json file is not found (FileNotFoundError)."""
        # Simulate a FileNotFoundError by setting the side effect
        mock_file.side_effect = FileNotFoundError

        # Instantiate the TTSAPI class
        vi = TTSAPI(self.api_key)

        # Verify that the file was attempted to be opened
        mock_file.assert_called_once_with(self.preferences_file, 'r')

        # Ensure that toggle_elevenlabs was set to False due to FileNotFoundError
        self.assertFalse(vi.toggle_elevenlabs)

    @patch('builtins.open', new_callable=mock_open)
    def test_get_elevenlabs_preference_json_decode_error(self, mock_file):
        """Test when preferences.json contains invalid JSON (JSONDecodeError)."""
        # Simulate invalid JSON content (missing closing brace)
        mock_file.return_value.read.return_value = '{invalid_json'  # Invalid JSON

        # Instantiate the TTSAPI class
        vi = TTSAPI(self.api_key)

        # Verify that the file was opened and read
        mock_file.assert_called_once_with(self.preferences_file, 'r')

        # Ensure that toggle_elevenlabs was set to False due to JSONDecodeError
        self.assertFalse(vi.toggle_elevenlabs)
        
class TestElevenlabs(unittest.TestCase):

    def setUp(self):
        # Patch get_elevenlabs_preference to return True (simulating ElevenLabs toggle being on)
        patch('api.tts_api.TTSAPI.get_elevenlabs_preference', return_value=True).start()
        
        # Initialize the TTSAPI class and set up the mocks
        self.api_key = "dummy_api_key"  # Replace with actual key if needed
        self.voice_interface = TTSAPI(self.api_key)
        self.voice_interface.engine = MagicMock()

        # Set toggle_elevenlabs to True to test that part of the code
        self.voice_interface.toggle_elevenlabs = True
        
        # Mock pygame methods
        patch('pygame.init').start()
        patch('pygame.mixer.music.load').start()
        patch('pygame.mixer.music.play').start()
        mock_get_busy = patch('pygame.mixer.music.get_busy').start()
        mock_get_busy.return_value = False
        patch('pygame.mixer.music.stop').start()
        patch('pygame.mixer.quit').start()

    def tearDown(self):
        patch.stopall()

    @patch('requests.post')  # Mocking the requests.post method
    def test_speak_with_elevenlabs(self, mock_post):
        # Simulate a successful response from the ElevenLabs API
        mock_response = MagicMock()
        mock_response.iter_content.return_value = [b"audio_data"]
        mock_post.return_value = mock_response
        
        # Call the speak function with test input
        text_to_speak = "Hello, this is a test!"
        self.voice_interface.speak(text_to_speak)
        
        # Assertions to check that the ElevenLabs API was called
        mock_post.assert_called_once_with(
            self.voice_interface.url,
            json={
                "text": text_to_speak,
                "model_id": "eleven_multilingual_v2",
                "voice_settings": {"stability": 0.5, "similarity_boost": 0.5}
            },
            headers=self.voice_interface.headers
        )
        
        # Check if pygame methods were called
        pygame.mixer.music.load.assert_called_once_with("output.mp3")
        pygame.mixer.music.play.assert_called_once()
        pygame.mixer.music.stop.assert_called_once()
        pygame.mixer.quit.assert_called_once()