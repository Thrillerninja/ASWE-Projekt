from typing import Dict

class IdleState:
    """
    State that represents the idle state/usecase of the application.
    """
    
    def __init__(self, state_machine):
        self.state_machine = state_machine
        self._running = True  # Add a flag to control the loop
        print("IdleState initialized")
        
    def on_enter(self):
        """
        Wait for a trigger to start the next usecase.
        """
        print("IdleState entered")
        
        while self._running:  # Use the flag to control the loop
            self.check_triggers()
            
    def check_triggers(self):
        """
        Check if a trigger is activated.
        """
        self.state_machine.start()
        
    def stop(self):
        """
        Stop the idle state loop.
        """
        self._running = False