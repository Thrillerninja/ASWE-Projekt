import pyttsx3
import speech_recognition as sr

class TTSAPI():
    """
    Class for text to speech and speech to text
    """
    def __init__(self):
        """
        Initializes the Interface
        """
        self.engine = pyttsx3.init(driverName='sapi5')
        
        voices = self.engine.getProperty('voices')
        # Set the voice to a specific German voice
        german_voice = next((voice for voice in voices if "de" in voice.languages), None)
        if german_voice:
            self.engine.setProperty('voice', german_voice.id)
        
        self.r = sr.Recognizer()
        
    def authenticate(self):
        """
        No authentication required
        """
        pass

    def speak(self, text: str):
        """
        Converts the input text into a voice output
        """
        if not isinstance(text, str) or not text.strip():
            raise ValueError("Text input must be a non-empty string.")
        
        self.engine.say(text)
        self.engine.runAndWait()
        
    def list_mics(self):
        """
        Lists all available microphones
        """
        mics = sr.Microphone.list_microphone_names()
        print("Available microphones:")
        for i, mic in enumerate(mics):
            print(f"{i}: {mic}")
        return mics

    def listen(self):
        """
        Listens for microphone input and returns a string of the speech input
        """
        try:
            with sr.Microphone() as source:
                self.speak("Ich höre zu...")
                self.r.adjust_for_ambient_noise(source)
                audio = self.r.listen(source)
                self.speak("Verarbeitung der Eingabe...")

                text = self.r.recognize_google(audio, language="de-DE")
                print(text)
                return text
        except sr.UnknownValueError:
            return "Google konnte das Audio nicht verstehen"
        except sr.RequestError as e:
            return f"Fehler bei der Anfrage an Google Speech Recognition; {0}".format(e)
        except Exception as e:
            return f"Ein Fehler ist aufgetreten: {str(e)}"
        
    def ask_yes_no(self, text: str):
        self.speak(text)
        response = self.listen()
        
        yes_alternatives = ['ja', 'jep', 'jo']
        no_alternatives = ['nein', 'ne']
        
        if any(x in response.lower() for x in yes_alternatives):
            return True 
        elif any(x in response.lower() for x in no_alternatives):
            return False
        else:
            return self.ask_yes_no("Entschuldigung, ich habe Ihre Antwort nicht verstanden. Bitte antworten Sie mit ja oder nein.")
        
        
    def play_sound(self, sound:str):
        """
        Plays a sound
        """
        print(f"Playing sound: {sound}")
        #TODO: Implement sound playing