import time

from loguru import logger
import time

from loguru import logger
from typing import Dict

class IdleState:
    """
    State that represents the idle state/usecase of the application.
    """
    _instance = None
    is_first_run = True
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(IdleState, cls).__new__(cls)
        return cls._instance
    _instance = None
    is_first_run = True
    
    def __init__(self, state_machine):
        if not hasattr(self, 'initialized'):  # Ensure __init__ is only called once
            self.state_machine = state_machine
            logger.info("IdleState initialized")
            self.initialized = True
        
    def on_enter(self):
        """
        Wait for a trigger to start the next usecase.
        """
        logger.info("IdleState entered")
        
        # Start Welcome Usecase on system startup
        if self.is_first_run and not self.state_machine.testing:
            # sleep for a second to lett the app start
            time.sleep(1)
            self.is_first_run = False
            self.state_machine.start()
        logger.info("IdleState entered")
        
        while not self.state_machine.testing:
            self.check_triggers()
            
    def check_triggers(self):
        """
        Check if a trigger is activated.
        """
        queue = self.state_machine.transition_queue
        if len(queue) > 0:
            trigger = queue.pop(0)
            self.state_machine.transition(trigger)