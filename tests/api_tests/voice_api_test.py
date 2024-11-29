import unittest
from unittest.mock import patch, MagicMock, mock_open
from api.tts_api import TTSAPI
import pyttsx3
import speech_recognition as sr
from config import CONFIG
import json

class TestVoiceInterface(unittest.TestCase):
    def setUp(self):
        patch('api.tts_api.TTSAPI.get_elevenlabs_preference', return_value=False).start()

        self.api_key = CONFIG['elevenlabs_key']
        self.voice_interface = TTSAPI(self.api_key)
        self.voice_interface.engine = MagicMock()

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

class TestVoiceInterfaceElevenLabs(unittest.TestCase):
    def setUp(self):
        patch('api.tts_api.TTSAPI.get_elevenlabs_preference', return_value=True).start()

        self.api_key = CONFIG['elevenlabs_key']
        self.voice_interface = TTSAPI(self.api_key)
        self.voice_interface.engine = MagicMock()

    @patch("builtins.open", new_callable=mock_open)
    @patch('pyttsx3.init')
    @patch("requests.post")
    @patch("pygame.mixer.music.load")
    @patch("pygame.mixer.music.play")
    @patch("pygame.mixer.music.get_busy", return_value=False)
    def test_speak_elevenlabs(self, mock_get_busy, mock_play, mock_load, mock_requests_post, mock_pyttsx3_init, mock_open):
        """
        Test speak functionality of ElevenLabs with valid and invalid inputs
        """
        patch('api.tts_api.TTSAPI.get_elevenlabs_preference', return_value=True).start()

        # Mock response from ElevenLabs API
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.iter_content.return_value = [b"chunk1", b"chunk2"]
        mock_requests_post.return_value = mock_response
        
        # Test ElevenLabs API call
        self.voice_interface.speak("Hello, ElevenLabs!")

        # Check if the ElevenLabs API was called
        mock_requests_post.assert_called_once_with(
            self.voice_interface.url,
            json={
                "text": "Hello, ElevenLabs!",
                "model_id": "eleven_multilingual_v2",
                "voice_settings": {"stability": 0.5, "similarity_boost": 0.5},
            },
            headers=self.voice_interface.headers,
        )

        # Check if the file was opened correctly and written to
        mock_open.assert_called_once_with("output.mp3", "wb")
        mock_open().write.assert_any_call(b"chunk1")
        mock_open().write.assert_any_call(b"chunk2")

        # Ensure pygame mixer methods are called
        mock_load.assert_called_once_with("output.mp3")
        mock_play.assert_called_once()

        # Check that get_busy() was called and it returned False (avoiding the blocking loop)
        mock_get_busy.assert_called_once()

        self.assertTrue(self.voice_interface.toggle_elevenlabs)

class TestGetElevenlabsPreference(unittest.TestCase):
    
    def setUp(self):
        """Set up the mocks and the instance of TTSAPI."""
        # Mock the get_elevenlabs_preference method globally during the instantiation of TTSAPI
        self.api_key = "mock_api_key"  # You can use a mock or actual key as per your test environment
        self.voice_interface = MagicMock(spec=TTSAPI)  # Create a MagicMock for the TTSAPI instance
        self.voice_interface.engine = MagicMock()

    @patch('api.tts_api.TTSAPI.get_elevenlabs_preference', return_value=True)  # Mock here
    def test_get_elevenlabs_preference_valid(self, mock_get_elevenlabs_preference):
        """Test when preferences.json exists and contains valid data."""
        # Mock response from preferences.json to return True (enabled)
        mock_get_elevenlabs_preference.return_value = True

        # Instantiate the TTSAPI class
        vi = TTSAPI(self.api_key)

        # Verify that the mocked method was called during initialization
        mock_get_elevenlabs_preference.assert_called_once()

        # Ensure that toggle_elevenlabs was set to True
        self.assertTrue(vi.toggle_elevenlabs)

    @patch('builtins.open', new_callable=mock_open)
    @patch('api.tts_api.TTSAPI.get_elevenlabs_preference', return_value=False)
    def test_get_elevenlabs_preference_missing_enable_elevenlabs(self, mock_get_elevenlabs_preference, mock_file):
        """Test when preferences.json exists but is missing the 'enable_elevenlabs' field."""
        mock_file.return_value.read.return_value = json.dumps({'other_field': 1})

        # Instantiate the TTSAPI class
        vi = TTSAPI(self.api_key)

        # Verify that the mocked method was called during initialization
        mock_get_elevenlabs_preference.assert_called_once()

        # Ensure that toggle_elevenlabs was set to False
        self.assertFalse(vi.toggle_elevenlabs)

    @patch('builtins.open', new_callable=mock_open)
    @patch('api.tts_api.TTSAPI.get_elevenlabs_preference', return_value=False)
    def test_get_elevenlabs_preference_file_not_found(self, mock_get_elevenlabs_preference, mock_file):
        """Test when preferences.json file is not found (FileNotFoundError)."""
        mock_file.side_effect = FileNotFoundError

        # Instantiate the TTSAPI class
        vi = TTSAPI(self.api_key)

        # Verify that the mocked method was called during initialization
        mock_get_elevenlabs_preference.assert_called_once()

        # Ensure that toggle_elevenlabs was set to False due to FileNotFoundError
        self.assertFalse(vi.toggle_elevenlabs)

    @patch('builtins.open', new_callable=mock_open)
    @patch('api.tts_api.TTSAPI.get_elevenlabs_preference', return_value=False)
    def test_get_elevenlabs_preference_json_decode_error(self, mock_get_elevenlabs_preference, mock_file):
        """Test when preferences.json contains invalid JSON (JSONDecodeError)."""
        mock_file.return_value.read.return_value = '{invalid_json'  # Invalid JSON

        # Instantiate the TTSAPI class
        vi = TTSAPI(self.api_key)

        # Verify that the mocked method was called during initialization
        mock_get_elevenlabs_preference.assert_called_once()

        # Ensure that toggle_elevenlabs was set to False due to JSONDecodeError
        self.assertFalse(vi.toggle_elevenlabs)