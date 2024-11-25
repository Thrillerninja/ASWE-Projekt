import pyttsx3
import speech_recognition as sr
from loguru import logger
import requests
import pygame

class TTSAPI():
    """
    Class for text to speech and speech to text
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(TTSAPI, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, api_key, toggle_elevenlabs: bool = False):
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
            
        # Set the microphone id
        self.mic_id = mic_id if mic_id is not None else self.get_first_active_mic_id()
        
        self.toggle_elevenlabs = toggle_elevenlabs
        
        self.r = sr.Recognizer()
        self.api_key = api_key
        pygame.init()
        self.CHUNK_SIZE = 1024
        self.url = "https://api.elevenlabs.io/v1/text-to-speech/pqHfZKP75CvOlQylNhV4"
        self.headers = {
              "Accept": "audio/mpeg",
              "Content-Type": "application/json",
              "xi-api-key": self.api_key
            }
        self.api_key = api_key
        pygame.init()
        self.CHUNK_SIZE = 1024
        self.url = "https://api.elevenlabs.io/v1/text-to-speech/pqHfZKP75CvOlQylNhV4"
        self.headers = {
              "Accept": "audio/mpeg",
              "Content-Type": "application/json",
              "xi-api-key": self.api_key
            }
        
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
        if self.toggle_elevenlabs:
            data = {
                "text": text,
                "model_id": "eleven_multilingual_v2",
                "voice_settings": {
                  "stability": 0.5,
                  "similarity_boost": 0.5
                }
            }
            response = requests.post(self.url, json=data, headers=self.headers)
            with open('output.mp3', 'wb') as f:
                for chunk in response.iter_content(chunk_size=self.CHUNK_SIZE):
                    if chunk:
                        f.write(chunk)
                        
            logger.info(f"Speaking text using Elevenlabs: {text}")
            
            pygame.mixer.music.load("output.mp3")
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pass
        else:    
            logger.info(f"Speaking text: {text}")
            self.engine.say(text)
            self.engine.runAndWait()
        
    def list_mics(self):
        """
        Lists all available microphones and indicates which ones are active or hearing sound.
        """
        logger.info("Listing available microphones")
        if hasattr(self, 'mics_listed') and self.mics_listed:
            return self.active_mics

        self.active_mics = []
        mics = sr.Microphone.list_microphone_names()
        print("Available microphones:")
        for i, mic in enumerate(mics):
            try:
                with sr.Microphone(device_index=i) as source:
                    self.r.adjust_for_ambient_noise(source)
                    audio = self.r.listen(source, timeout=1)
                    print(f"{i}: {mic} (active)")
                    self.active_mics.append(i)
            except sr.WaitTimeoutError:
                print(f"{i}: {mic} (inactive)")
            except AttributeError:
                print(f"{i}: {mic} (error: 'NoneType' object has no attribute 'close')")
            except Exception as e:
                logger.error(f"{i}: {mic} (error: {e})")
                
        print(f"Active microphones: {self.active_mics}")
        self.mics_listed = True
        return self.active_mics

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
                self.r.adjust_for_ambient_noise(source)
                audio = self.r.listen(source, timeout=timeout)
                self.speak("Verarbeitung der Eingabe...")

                logger.info("Listening for microphone input")
                text = self.r.recognize_google(audio, language="de-DE")
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
