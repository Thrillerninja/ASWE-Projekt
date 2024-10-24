import pyttsx3
import speech_recognition as sr

class VoiceInterface():
    """
    Class for text to speech and speech to text
    """
    def __init__(self):
        """
        Initializes the Interface
        """
        self.engine = pyttsx3.init()

        self.r = sr.Recognizer()
        
    def authenticate(self):
        """
        No authentication required
        """
        pass

    def speak(self, text:str):
        """
        Converts the input text into a voice output
        """
        if not isinstance(text, str) or not text.strip():
            raise ValueError("Text input must be a non-empty string.")
        
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        """
        Listens for microphone input and returns a string of the speech input
        """
        try:
            with sr.Microphone() as source:
                self.r.adjust_for_ambient_noise(source)
                audio = self.r.listen(source)

                text = self.r.recognize_google(audio, language="de-DE")
                return text
        except sr.UnknownValueError:
            return "Google konnte das Audio nicht verstehen"
        except sr.RequestError as e:
            return f"Fehler bei der Anfrage an Google Speech Recognition; {0}".format(e)
        except Exception as e:
            return f"Ein Fehler ist aufgetreten: {str(e)}"