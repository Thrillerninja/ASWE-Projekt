from typing import Dict

class IdleState:
    """
    State that represents the idle state/usecase of the application.
    """
    
    def __init__(self, state_machine):
        self.state_machine = state_machine
        print("IdleState initialized")
        
    def on_enter(self):
        """
        Wait for a trigger to start the next usecase.
        """
        print("IdleState entered")
        
        while True:
            self.check_triggers()
            
    def check_triggers(self):
        """
        Check if a trigger is activated.
        """
        trigger = input("Press 's' to start the next usecase: ")
        if trigger == 's':
            self.state_machine.start()
            return
        else:
            print("Invalid input. Please try again.")