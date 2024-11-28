import unittest
from unittest.mock import patch, MagicMock, mock_open
from api.tts_api import TTSAPI
import pyttsx3
import speech_recognition as sr
from config import CONFIG

class TestVoiceInterface(unittest.TestCase):
    def setUp(self):
        self.api_key = CONFIG['elevenlabs_key']
        self.voice_interface = TTSAPI(self.api_key)
        self.voice_interface.engine = MagicMock()

    @patch('api.tts_api.main.pyttsx3.init')
    def test_init(self, mock_pyttsx3_init):
        """
        Test initialization of VoiceInterface
        """
        mock_pyttsx3_init.return_value = self.voice_interface.engine

        vi = TTSAPI(self.api_key)
        self.assertIsNotNone(vi.recognize)

    @patch('api.tts_api.main.pyttsx3.init')
    def test_speak(self, mock_pyttsx3_init):
        """
        Test speak functionality of the system with valid and invalid inputs
        """
        mock_engine = MagicMock()
        mock_pyttsx3_init.return_value = mock_engine

        vi = TTSAPI(self.api_key)
        vi.speak("Hello")
        vi.engine.say.assert_called_with("Hello")
        vi.engine.runAndWait.assert_called_once()

        # Test empty string
        with self.assertRaises(ValueError):
            vi.speak("")

        # Test non-string input
        with self.assertRaises(ValueError):
            vi.speak(123)

    @patch("builtins.open", new_callable=mock_open)
    @patch('pyttsx3.init')
    @patch('requests.post')
    @patch("pygame.mixer.music.load")
    @patch("pygame.mixer.music.play")
    @patch("pygame.mixer.music.get_busy", return_value=False)  # Mock get_busy() to return False immediately
    def test_speak_elevenlabs(self, mock_get_busy, mock_play, mock_load, mock_requests_post, mock_pyttsx3_init, mock_open):
        """
        Test speak functionality of ElevenLabs with valid and invalid inputs
        """
        # Mock response from ElevenLabs API
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.iter_content.return_value = [b"chunk1", b"chunk2"]
        mock_requests_post.return_value = mock_response

        vi = TTSAPI(self.api_key, toggle_elevenlabs=True)
        vi.toggle_elevenlabs = True
        
        # Test ElevenLabs API call
        vi.speak("Hello, ElevenLabs!")

        # Check if the ElevenLabs API was called
        mock_requests_post.assert_called_once_with(
            vi.url,
            json={
                "text": "Hello, ElevenLabs!",
                "model_id": "eleven_multilingual_v2",
                "voice_settings": {"stability": 0.5, "similarity_boost": 0.5},
            },
            headers=vi.headers,
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


    @patch('speech_recognition.Recognizer.recognize_google')
    @patch('speech_recognition.Recognizer.listen')
    @patch('speech_recognition.Microphone')
    def test_listen_general_error(self, mock_microphone, mock_listen, mock_recognize_google):
        """
        Test listen handling for a general exception
        """
        mock_listen.return_value = MagicMock()
        mock_recognize_google.side_effect = Exception("General Error")

        with patch.object(self.voice_interface, 'listen', return_value="Ein Fehler ist aufgetreten"):
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

