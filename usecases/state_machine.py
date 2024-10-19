from transitions import Machine, State
from .idle_state import IdleState
from .welcome_state import WelcomeState

class StateMachine:
    """
    State machine that controls the flow of the application.
    """
    
    # Define states
    states = [
        State(name='idle', on_enter='on_enter'),
        State(name='welcome', on_enter='on_enter')
    ]
    
    def __init__(self):
        print("StateMachine initialized")
        self.machine = Machine(model=self, states=self.states, initial='idle')
        
        # Initialize states
        self.idle = IdleState(self)
        self.welcome = WelcomeState(self)
        
        # Setup transitions
        self.machine.add_transition('start', 'idle', 'welcome')
        self.machine.add_transition('exit', 'welcome', 'idle')
        
        # Initialize API clients
        self.api_clients = {}
        
        # Transition to initial state
        # to_ is a method provided by transitions to call the transition appended
        self.to_idle()
        
    def on_enter(self):
        """
        Callback method that is called when entering a state.
        It maps the current state to the corresponding state object and calls its on_enter method.
        """
        # Get the current state and map it to the corresponding state object
        stateDict = {
            'idle': self.idle,
            'welcome': self.welcome
        }
        # Call the on_enter method of the state object
        stateDict[self.state].on_enter()