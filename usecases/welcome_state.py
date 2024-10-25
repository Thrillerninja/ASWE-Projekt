from typing import Dict
import datetime
from api.api_factory import APIFactory

class WelcomeState:
    """
    State that represents the welcome state/usecase of the application.
    """
    
    def __init__(self, state_machine):
        self.state_machine = state_machine
        
        self.t2s_api = self.state_machine.api_factory.create_api(api_type="t2s")
        self.transit_api = None # TODO: Replace with transit API object
        self.weather_api = self.state_machine.api_factory.create_api(api_type="weather")
        self.rapla_api = self.state_machine.api_factory.create_api(api_type="rapla")
        
        self.default_wakeup_time = datetime.time(9, 0)  # TODO: Replace with preferences file value
        
        
        print("WelcomeState initialized")
    
    def on_enter(self):
        """
        Function executed when the state is entered.
        It sets up the alarm, retrieves the weather forecast, and informs the user about their schedule.
        """
        print("WelcomeState entered")
        
        # Calculate wake-up time based on the first calendar appointment
        wakeup_time = self.calc_alarm_time()
        print(f"Wake-up time set for: {wakeup_time}")

        # TODO: Set the alarm using the calculated wakeup_time

        # Retrieve and provide the current weather forecast
        weather_forecast = self.weather_api.get_forecast()
        self.t2s_api.speak(f"Good morning! It's {datetime.datetime.now().strftime('%H:%M')} The weather forecast for today is: {weather_forecast}")
        
        # Provide the user with the information about their first appointment
        first_appointment = self.rapla_api.get_todays_appointments()[0]
        self.t2s_api.speak(f"Your first appointment is at {first_appointment.start} in {first_appointment.room}.")
        
        # Ask the user if they want to start the next use case (e.g., Nachrichtenassistent)
        user_response = self.t2s_api.ask_yes_no("Would you like to hear the news?")
        if user_response:
            self.state_machine.transition_to("morning_news")
        else:
            self.t2s_api.speak("Okay, let me know if you need anything!")
        
    def calc_alarm_time(self):
        """
        Calculate the time for the alarm clock based on the first appointment of the user's calendar.
        """
        
        # Retrieve user's calendar entries for the next day 
        calendar_entries = self.rapla_api.get_todays_appointments()
        
        if calendar_entries == None:
            return self.default_wakeup_time
        
        first_appointment = calendar_entries[0]        
        

        # Route to the appointment location is determined using the navigation service (address from preferences file) 
        # ...
        # ...
        transit_time = 30 # result of the routing service
     
        # Calculate required time for alarm clock 
        first_appointment_time = datetime.datetime.strptime(first_appointment.start, "%H:%M").time()
        # Check second alternative process and set latest alarm time to be no later than default_wakeup_time        
        if first_appointment_time > self.default_wakeup_time:
            return self.default_wakeup_time
        
        return first_appointment_time - datetime.timedelta(minutes=transit_time)