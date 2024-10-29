import datetime
from typing import Dict

class SpeachState:
    """
    State that represents the speech recognition state/use case of the application.
    """

    def __init__(self, state_machine):
        self.state_machine = state_machine
        self.voice_interface = state_machine.api_factory.create_api(api_type="tts")
        print("SpeachState initialized")

    def on_enter(self):
        """
        Start the speech recognition.
        """
        print("SpeachState entered")
        self.voice_interface.speak("Bitte sprechen Sie einen Befehl.")
        
        start_time = datetime.datetime.now().timestamp()
        while  datetime.datetime.now().timestamp() - start_time < 10:
            self.check_triggers()
        
        self.voice_interface.play_sound("idle")
        
    def check_triggers(self):
        """
        Listens for user input and determines the next action.
        """
        user_input = self.voice_interface.listen()
        print(f"User said: {user_input}")
        
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
            self.voice_interface.speak("Befehl nicht erkannt. Bitte versuchen Sie es erneut.")
