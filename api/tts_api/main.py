import pyttsx3
import requests
import speech_recognition as sr
from loguru import logger
import threading
import pygame
import numpy as np


class TTSAPI:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(TTSAPI, cls).__new__(cls)
            cls._instance.__initialized = False
        return cls._instance

    def __init__(self, api_key, state_machine):
        if self.__initialized:
            return
        
        self.state_machine = state_machine
        
        self.__initialized = True

        try:
            self.engine = pyttsx3.init(driverName='sapi5')
        except ImportError:
            self.engine = pyttsx3.init()
        except Exception as e:
            logger.error(f"Error initializing pyttsx3: {e}")

        voices = self.engine.getProperty('voices')
        german_voice = next((voice for voice in voices if "de" in voice.languages), None)
        if german_voice:
            self.engine.setProperty('voice', german_voice.id)

        self.recognize = sr.Recognizer()
        
        self.engine_lock = threading.Lock()  # Add a lock for the engine
        
        self.toggle_elevenlabs = bool(self.state_machine.preferences["enable_elevenlabs"])
        
        self.api_key = api_key

        self.CHUNK_SIZE = 1024
        self.url = "https://api.elevenlabs.io/v1/text-to-speech/pqHfZKP75CvOlQylNhV4"
        self.headers = {
              "Accept": "audio/mpeg",
              "Content-Type": "application/json",
              "xi-api-key": self.api_key
            }

    def beep(self):
        frequency = 900  # Frequenz in Hertz
        duration = 0.5    # Dauer in Sekunden
        sample_rate = 44100  # Abtastrate
        pygame.mixer.init(frequency=sample_rate, size=-16, channels=1)
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        wave = 0.5 * np.sin(2 * np.pi * frequency * t)
        wave = (wave * 32767).astype(np.int16).tobytes()
        sound = pygame.mixer.Sound(buffer=wave)
        sound.play()
        pygame.time.wait(int(duration * 1000))
        pygame.mixer.quit()

    def authenticate(self):
        """
        No authentication required
        """
        pass
      
      
   
    def list_mics(self):
        """
        Lists all available microphones
        """
        mics = sr.Microphone.list_microphone_names()
        print("Available microphones:")
        for i, mic in enumerate(mics):
            print(f"{i}: {mic}")
        return mics
    

    def get_specific_micindex_by_name(self, mic_name_part:str):
        mics = sr.Microphone.list_microphone_names()
        for i, mic in enumerate(mics):
            if mic_name_part.lower() in mic.lower():
                return i

    def speak(self, text: str):
        """
        Converts the input text into a voice output
        """
        if not isinstance(text, str) or not text.strip():
            raise ValueError("Text input must be a non-empty string.")

        if self.toggle_elevenlabs:
            # Restart the pygame mixer to avoid issues with the sound output
            pygame.init()
            
            data = {
                "text": text,
                "model_id": "eleven_multilingual_v2",
                "voice_settings": {
                  "stability": 0.5,
                  "similarity_boost": 0.5
                }
            }
            response = requests.post(self.url, json=data, headers=self.headers)
            response.raise_for_status()
            try:
                with open('output.mp3', 'wb') as f:
                    for chunk in response.iter_content(chunk_size=self.CHUNK_SIZE):
                        if chunk:
                            f.write(chunk)
                            
                logger.info(f"Speaking text using Elevenlabs: {text}")
                
                pygame.mixer.music.load("output.mp3")
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    pass
            except Exception as e:
                logger.error(f"Error during speaking with Elevenlabs: {e}")
            finally:
                pygame.quit()
        else:    
            logger.debug(f"Speaking text: {text}")
            with self.engine_lock:  # Use the lock to ensure only one thread accesses the engine at a time
                self.engine.say(text)
            self.engine.runAndWait()


    def listen(self, timeout=None):
        try:
            mic_index = self.state_machine.preferences["mic_id"] or self.get_specific_micindex_by_name("jabra") or 1
            with sr.Microphone(device_index=mic_index) as source:
                self.recognize.adjust_for_ambient_noise(source)
                self.beep()
                logger.info(f"Listening for microphone input on mic_id {self.state_machine.preferences['mic_id']}")
                audio = self.recognize.listen(source, timeout=timeout)
                text = self.recognize.recognize_google(audio, language="de-DE")
                logger.info(f"Recognized text: {text}")
                return text
        except sr.UnknownValueError:
            return "Google konnte das Audio nicht verstehen"
        except sr.RequestError as e:
            return f"Fehler bei der Anfrage an Google Speech Recognition; {e}"
        except Exception as e:
            logger.error(f"Error during listening: {e}")
            return f"Ein Fehler ist aufgetreten: {e}"
        
    def listen_continuous(self, callback, timeout=5):
        """
        Continuously listen for user input and call the callback function with the recognized text.
        """
        logger.info(f"Listening for microphone input on mic_id {self.state_machine.preferences['mic_id']}")
        i = 0
        while True:
            try:
                with sr.Microphone(device_index=self.state_machine.preferences["mic_id"]) as source:
                    self.recognize.adjust_for_ambient_noise(source)
                    self.beep()

                    audio = self.recognize.listen(source, timeout=timeout)
                    text = self.recognize.recognize_google(audio, language="de-DE")
                    callback(text)
            except sr.UnknownValueError:
                callback("Google konnte das Audio nicht verstehen")
            except sr.RequestError as e:
                callback(f"Fehler bei der Anfrage an Google Speech Recognition; {e}")
            except Exception as e:
                logger.error(f"Error during listening: {e}")
                callback(f"Ein Fehler ist aufgetreten: {e}")
            if i > 5:
                callback("test text")
                break
            i = i + 1
        
    def ask_yes_no(self, text, retries=3, timeout=5):
        """
        Ask the user a yes/no question and return True for yes and False for no.
        Retries the question up to a specified number of times if the response is not understood.
        """
        for _ in range(retries):
            self.speak(text)
            response = self.listen(timeout=timeout)  # Pass the timeout to the listen method
            
            if response:
                words = response.lower().split()  # Split the response into individual words
                if any(word in ['ja', 'yes'] for word in words):  # Check for a singular match
                    return True
                if any(word in ['nein', 'no'] for word in words):  # Check for a singular match
                    return False
            # If no valid word is found, ask again
            text = "Entschuldigung, ich habe Ihre Antwort nicht verstanden. Bitte antworten Sie mit ja oder nein."
        return False
        
    def play_sound(self, sound:str):
        """
        Plays a sound
        """
        logger.debug(f"Playing sound: {sound}")
        
        if sound == "mic_activation":
            sound_path = "config/sounds/mic_activation.wav"
        else:
            sound_path = sound
        
        try:
            pygame.init()  # Initialize pygame
            pygame.mixer.init()  # Initialize the mixer
            pygame.mixer.music.load(sound_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pass
        except Exception as e:
            logger.error(f"Error playing ping sound: {e}")
        finally:
            pygame.mixer.quit()  # Quit the mixer after playing the sound