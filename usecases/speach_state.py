from typing import Dict

class SpeachState:
    """
    State that represents the speach state/usecase of the application.
    """
    
    def __init__(self, state_machine):
        self.state_machine = state_machine
        print("SpeachState initialized")
        
    def on_enter(self):
        """
        Start the speach recognition.
        """
        print("SpeachState entered")
        
        while True:
            self.check_triggers()
            
    def check_triggers(self):
        """
        Check if a trigger is activated.
        """
        trigger = input("Press 'e' to exit the speach recognition: ")
        if trigger == 'e':
            self.state_machine.exit()
            return
        else:
            print("Invalid input. Please try again.")