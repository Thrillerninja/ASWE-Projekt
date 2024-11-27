import datetime
from typing import Dict

class SpeachState:
    """
    State that represents the speech recognition state/use case of the application.
    """

    def __init__(self, state_machine):
        self.state_machine = state_machine
        self.voice_interface = state_machine.api_factory.create_api(api_type="tts")
        self.running = True
        self.testing = False
        self.retry_count = 0  # Add a retry counter
        print("SpeachState initialized")

    def on_enter(self):
        """
        Start the speech recognition.
        """
        print("SpeachState entered")
        self.voice_interface.speak("Bitte sprechen Sie einen Befehl.")
        
        
        self.voice_interface.listen_continuous(self.process_input, timeout=5)
        
        self.voice_interface.play_sound("idle")
        self.voice_interface.speak("Spracherkennung beendet.")

    def process_input(self, user_input):
        """
        Check for specific voice commands and trigger corresponding state transitions.
        """
        user_input = self.voice_interface.listen()
        self.process_input(user_input)

    def process_input(self, user_input):
        """
        Check for specific voice commands and trigger corresponding state transitions.
        """
        user_input = self.voice_interface.listen()
        self.process_input(user_input)

    def process_input(self, user_input):
        """
        Check for specific voice commands and trigger corresponding state transitions.
        """
        user_input = self.voice_interface.listen()
        self.process_input(user_input)

    def process_input(self, user_input):
        """
        Check for specific voice commands and trigger corresponding state transitions.
        """
        user_input = self.voice_interface.listen()
        self.process_input(user_input)

    def process_input(self, user_input):
        """
        Process the user input and determine the next action.
        """
        if not user_input:
            self.voice_interface.speak("Keine Eingabe erkannt. Bitte versuchen Sie es erneut.")
            return
        
        print(f"User said: {user_input}")
        if self.testing:
            self.running = False            
        
        # Interpret the user's input and trigger the appropriate state transition
        if "beenden" in user_input.lower() or "exit" in user_input.lower():
            self.voice_interface.speak("Spracherkennung wird beendet.")
            self.state_machine.goto_idle()

        elif "willkommen" in user_input.lower() or "welcome" in user_input.lower():
            self.voice_interface.speak("Wechsel zu Willkommensnachricht.")
            self.state_machine.goto_welcome()
        
        elif "finanzen" in user_input.lower() or "finance" in user_input.lower():
            self.voice_interface.speak("Wechsel zu Finanzinformationen.")
            self.state_machine.goto_finance()
        
        elif "nachrichten" in user_input.lower() or "news" in user_input.lower():
            self.voice_interface.speak("Wechsel zu Nachrichten.")
            self.state_machine.goto_news()
        
        elif "aktivitäten" in user_input.lower() or "activities" in user_input.lower():
            self.voice_interface.speak("Wechsel zu Aktivitäten.")
            self.state_machine.goto_activity()
        
        else:
            self.retry_count += 1
            if self.retry_count < 3:
                self.voice_interface.speak("Befehl nicht erkannt. Bitte versuchen Sie es erneut.")
            else:
                self.voice_interface.speak("Die Spracherkennung wird beendet.")
                self.state_machine.goto_idle()
            self.retry_count += 1
            if self.retry_count < 3:
                self.voice_interface.speak("Befehl nicht erkannt. Bitte versuchen Sie es erneut.")
            else:
                self.voice_interface.speak("Die Spracherkennung wird beendet.")
                self.state_machine.goto_idle()