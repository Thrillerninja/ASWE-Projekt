from typing import Dict

class WelcomeState:
    """
    State that represents the welcome state/usecase of the application.
    """
    
    def __init__(self, state_machine):
        self.state_machine = state_machine
        print("WelcomeState initialized")
        
    def on_event(self, event, event_data):
        print("WelcomeState event: " + event)
        if event == 'exit':
            return self.state_machine.idle
        return
    
    def on_enter(self):
        print("WelcomeState entered")
        self.state_machine.exit()
        