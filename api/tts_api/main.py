import pyttsx3
import speech_recognition as sr
from loguru import logger

class TTSAPI():
    """
    Class for text to speech and speech to text
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(TTSAPI, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, mic_id=None):
        """
        Initializes the Interface
        """
        try:
            self.engine = pyttsx3.init(driverName='sapi5')
        except ImportError:
            self.engine = pyttsx3.init()
        except Exception as e:
            logger.error(f"Error initializing pyttsx3: {e}")
        
        voices = self.engine.getProperty('voices')
        # Set the voice to a specific German voice
        german_voice = next((voice for voice in voices if "de" in voice.languages), None)
        if german_voice:
            self.engine.setProperty('voice', german_voice.id)
            
        # Set the active microphone id
        self.recogize = sr.Recognizer()
        self.mic_id = mic_id if mic_id is not None else self.get_first_active_mic_id()
    
        
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
        
        logger.info(f"Speaking text: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
        
    def list_mics(self, timeout=1):
        mics = sr.Microphone.list_microphone_names()
        active_mics = []
        for i, mic in enumerate(mics):
            try:
                with sr.Microphone(device_index=i) as source:
                    self.recogize.adjust_for_ambient_noise(source, duration=0.5)
                    logger.info(f"Microphone {i}: {mic} is active")
                    active_mics.append((i, mic))
            except Exception as e:
                logger.warning(f"Microphone {i} ({mic}) error: {e}")
                
        if not active_mics:
            logger.error("No microphones found")
            # Throw an error if no active microphones are found
            raise Exception("No active microphones found")
            
        logger.success(f"Active microphones: {active_mics}")        
        return active_mics

    def get_first_active_mic_id(self):
        """
        Returns the ID of the first active microphone.
        """
        active_mics = self.list_mics()
        if active_mics:
            return active_mics[0]  # Return the index of the first active mic
        return 0  # Default to the first mic if no active mic is found

    def set_mic_id(self, mic_id: int):
        """
        Sets the microphone ID.
        """
        self.mic_id = mic_id
        
    def listen(self, timeout=None):
        """
        Listens for microphone input and returns a string of the speech input.
        """
        try:
            with sr.Microphone(device_index=self.mic_id) as source:
                self.recogize.adjust_for_ambient_noise(source)
                audio = self.recogize.listen(source, timeout=timeout)
                self.speak("Verarbeitung der Eingabe...")

                logger.info("Listening for microphone input")
                text = self.recogize.recognize_google(audio, language="de-DE")
                print(text)
                return text
        except sr.UnknownValueError:
            return "Google konnte das Audio nicht verstehen"
        except sr.RequestError as e:
            return f"Fehler bei der Anfrage an Google Speech Recognition; {0}".format(e)
        except Exception as e:
            logger.error(f"Error during listening: {str(e)}")
            return f"Ein Fehler ist aufgetreten: {str(e)}"
        
    def ask_yes_no(self, text, retries=3, timeout=5):
        """
        Ask the user a yes/no question and return True for yes and False for no.
        Retries the question up to a specified number of times if the response is not understood.
        """
        for _ in range(retries):
            self.speak(text)
            response = self.listen(timeout=timeout)  # Pass the timeout to the listen method
            if response.lower() in ['ja', 'yes']:
                return True
            elif response.lower() in ['nein', 'no']:
                return False
            else:
                text = "Entschuldigung, ich habe Ihre Antwort nicht verstanden. Bitte antworten Sie mit ja oder nein."
        return False
        
    def play_sound(self, sound:str):
        """
        Plays a sound
        """
        print(f"Playing sound: {sound}")
        #TODO: Implement sound playing
