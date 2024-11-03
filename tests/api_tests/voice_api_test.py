import unittest
from unittest.mock import patch, MagicMock
from api.tts_api import VoiceInterface
import pyttsx3
import speech_recognition as sr

class TestVoiceInterface(unittest.TestCase):
    def setUp(self):
        self.voice_interface = VoiceInterface()

    @patch('pyttsx3.init')
    def test_init(self, mock_pyttsx3_init):
        """
        Test initialization of VoiceInterface
        """
        mock_engine = MagicMock()
        mock_pyttsx3_init.return_value = mock_engine

        vi = VoiceInterface()
        mock_pyttsx3_init.assert_called_once()
        self.assertIsNotNone(vi.r)

    @patch('pyttsx3.Engine')
    def test_speak(self, mock_engine):
        """
        Test speak functionality with valid and invalid inputs
        """
        mock_engine = MagicMock()
        self.voice_interface.engine = mock_engine

        self.voice_interface.speak("Hello")
        mock_engine.say.assert_called_with("Hello")
        mock_engine.runAndWait.assert_called_once()

        # Test empty string
        with self.assertRaises(ValueError):
            self.voice_interface.speak("")

        # Test non-string input
        with self.assertRaises(ValueError):
            self.voice_interface.speak(123)

    @patch('speech_recognition.Recognizer.recognize_google')
    @patch('speech_recognition.Recognizer.listen')
    @patch('speech_recognition.Microphone')
    def test_listen_general_error(self, mock_microphone, mock_listen, mock_recognize_google):
        """
        Test listen handling for a general exception
        """
        mock_audio = MagicMock()
        mock_listen.return_value = mock_audio
        mock_recognize_google.side_effect = Exception("General Error")

        result = self.voice_interface.listen()
        self.assertIn("Ein Fehler ist aufgetreten", result)
        
    def test_yes_no(self):
        """
        Test ask_yes_no functionality
        """
        with patch.object(self.voice_interface, 'speak') as mock_speak:
            with patch.object(self.voice_interface, 'listen') as mock_listen:
                mock_listen.return_value = "yes"
                self.assertTrue(self.voice_interface.ask_yes_no("Do you like ice cream?"))
                mock_speak.assert_called_with("Do you like ice cream?")

                mock_listen.return_value = "no"
                self.assertFalse(self.voice_interface.ask_yes_no("Do you like ice cream?"))
                mock_speak.assert_called_with("Do you like ice cream?")

                mock_listen.return_value = "I don't know"
                self.assertFalse(self.voice_interface.ask_yes_no("Do you like ice cream?"))
                mock_speak.assert_called_with("Do you like ice cream?")
