from transitions import Machine, State
from config import CONFIG
from api.api_factory import APIFactory
from .idle_state import IdleState
from .welcome_state import WelcomeState
from .speach_state import SpeachState

class StateMachine:
    """
    State machine that controls the flow of the application.
    """
    
    # Define states
    states = [
        State(name='idle', on_enter='on_enter'), # on_enter is a callback method that is called when entering the state (calls the func in this class)
        State(name='welcome', on_enter='on_enter'),
        State(name='speach', on_enter='on_enter'),
        State(name='news', on_enter='on_enter'),
        State(name='finance', on_enter='on_enter'),
        State(name='activity', on_enter='on_enter'),
    ]
    
    def __init__(self):
        print("StateMachine initialized")
        self.machine = Machine(model=self, states=self.states, initial='idle')
        
        self.api_factory = APIFactory(CONFIG)
        
        # Initialize states
        self.idle = IdleState(self)
        self.welcome = WelcomeState(self)
        self.speach = SpeachState(self)
        self.news = None # TODO: Replace with NewsState object
        self.finance = None
        self.activity = None
        
        # Setup transitions
        self.machine.add_transition('start', 'idle', 'welcome')
        self.machine.add_transition('exit', 'welcome', 'idle')
        
        self.machine.add_transition(trigger='interact', source='idle', dest='speach')
        self.machine.add_transition(trigger='morning_news', source='welcome', dest='news')
        self.machine.add_transition(trigger='interaction', source="welcome", dest='speach')
        
        self.machine.add_transition(trigger='exit', source='speach', dest='idle')
        self.machine.add_transition(trigger='goto_welcome', source='speach', dest='welcome')
        self.machine.add_transition(trigger='goto_finance', source='speach', dest='finance')
        self.machine.add_transition(trigger='goto_activity', source='speach', dest='activity')
        self.machine.add_transition(trigger='goto_news', source='speach', dest='news')
        
        
        # Transition to initial state
        # to_ is a method provided by transitions to call the transition appended
        self.to_idle()
        
    def on_enter(self):
        """
        Callback method that is called when entering a state.
        It maps the current state to the corresponding state object and calls its on_enter method.
        """
        # Get the current state and map it to the corresponding state object
        state_dict = {
            'idle': self.idle,
            'welcome': self.welcome,
            'speach': self.speach,
            'news': self.news,
            'finance': self.finance,
            'activity': self.activity,
        }
        # Call the on_enter method of the state object
        state_dict[self.state].on_enter()
