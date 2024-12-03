from loguru import logger
from transitions import Machine, State
from config import CONFIG
from frontend.config_manager import load_preferences_file
from PyQt5.QtCore import QObject, pyqtSignal
from api.api_factory import APIFactory
from usecases.activity_state import ActivityState
from .idle_state import IdleState
from .welcome_state import WelcomeState
from .speach_state import SpeachState
from frontend.config_manager import load_preferences_file
from .news_state import NewsState
from.financetracker_state import FinanceState
from .news_state import NewsState
from.financetracker_state import FinanceState

class StateMachine(QObject):
    """
    State machine that controls the flow of the application.
    """
    # Signal that is emitted when the state changes (used to inform the frontend)
    state_changed = pyqtSignal(str)
    
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
        super(StateMachine, self).__init__()  # Call the superclass __init__ method
        
        logger.info("StateMachine initialized")
        self.machine = Machine(model=self, states=self.states, initial='idle')
        
        self.testing = False
        self.running = True
        
        self.transition_queue = []

        # User preferences, hover over function to see details. This dictionary is kept up to date with the frontend.
        self.preferences = load_preferences_file()
        self.testing = False

        # User preferences, hover over function to see details. This dictionary is kept up to date with the frontend.
        self.preferences = load_preferences_file()
        
        self.api_factory = APIFactory(CONFIG)
        
        # Initialize states
        self.idle = IdleState(self)
        self.welcome = WelcomeState(self)
        self.speach = SpeachState(self)
        self.news =  NewsState(self)
        self.finance = FinanceState(self)
        self.activity = ActivityState(self)
        
        # Setup transitions
        self.machine.add_transition('start', 'idle', 'welcome')
        self.machine.add_transition('exit', 'welcome', 'idle')
        
        self.machine.add_transition(trigger='news_interact', source="news", dest='speach')
        self.machine.add_transition(trigger='news_idle', source="news", dest='idle')
        self.machine.add_transition(trigger='news_interact', source="news", dest='speach')
        self.machine.add_transition(trigger='news_idle', source="news", dest='idle')
        self.machine.add_transition(trigger='interact', source='idle', dest='speach')
        self.machine.add_transition(trigger='morning_news', source='welcome', dest='news')
        self.machine.add_transition(trigger='interaction', source="welcome", dest='speach')
        self.machine.add_transition(trigger='activity_idle', source="activity", dest='idle')

        self.machine.add_transition(trigger='goto_idle', source='speach', dest='idle')
        self.machine.add_transition(trigger='goto_idle', source='speach', dest='idle')
        self.machine.add_transition(trigger='goto_welcome', source='speach', dest='welcome')
        self.machine.add_transition(trigger='goto_finance', source='speach', dest='finance')
        self.machine.add_transition(trigger='goto_activity', source='idle', dest='activity')
        self.machine.add_transition(trigger='goto_news', source='speach', dest='news')
        
        self.machine.add_transition(trigger='goto_finance', source='speach', dest='finance')
        self.machine.add_transition(trigger='exit_finance', source='finance', dest='idle')

    def some_trigger_for_state(self):
        # Logic to transition to the desired state
        print("Initialization complete. Transitioning to the next state...")

    def stop(self):
        """
        Stop the state machine.
        """
        self.running = False
        print("State machine stopped")
        
    def queue_transition(self, transition: str):
        """Queue a transition to be executed when the current state is idle."""
        logger.info(f"Queueing transition: {transition}")
        if self.state == 'idle':
            getattr(self, transition)()
        else:
            self.transition_queue.append(transition)

    def stop(self):
        """
        Stop the state machine.
        """
        self.running = False
        print("State machine stopped")
        
    def queue_transition(self, transition: str):
        """Queue a transition to be executed when the current state is idle."""
        logger.info(f"Queueing transition: {transition}")
        if self.state == 'idle':
            getattr(self, transition)()
        else:
            self.transition_queue.append(transition)

    def on_enter(self):
        """
        Callback method that is called when entering a state.
        It maps the current state to the corresponding state object and calls its on_enter method.
        """
        logger.info(f"Entering state: {self.state}")
        # Get the current state and map it to the corresponding state object
        state_dict = {
            'idle': self.idle,
            'welcome': self.welcome,
            'speach': self.speach,
            'news': self.news,
            'finance': self.finance,
            'activity': self.activity,
        }
        # Inform the frontend about the state change
        self.state_changed.emit(self.state)
        # Call the on_enter method of the state object
        state_dict[self.state].on_enter()
        # Process queued transitions if the current state is idle
        if self.state == 'idle' and self.transition_queue:
            next_transition = self.transition_queue.pop(0)
            getattr(self, next_transition)()
