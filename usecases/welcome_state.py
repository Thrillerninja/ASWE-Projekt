from typing import Dict
import datetime
from unittest.mock import MagicMock
from loguru import logger
from api.api_factory import APIFactory

class WelcomeState:
    """
    State that represents the welcome state/usecase of the application.
    """
    
    def __init__(self, state_machine):
        self.state_machine = state_machine
        
        self.tts_api = self.state_machine.api_factory.create_api(api_type="tts")
        self.transit_api = None # TODO: Replace with transit API object
        self.weather_api = self.state_machine.api_factory.create_api(api_type="weather")
        self.rapla_api = self.state_machine.api_factory.create_api(api_type="rapla")
        
        default_alarm_time = self.state_machine.preferences.get("default_alarm_time", "09:00")
        if isinstance(default_alarm_time, MagicMock):
            default_alarm_time = "09:00"
        self.default_wakeup_time = datetime.datetime.strptime(default_alarm_time, "%H:%M").time()
        
        logger.info("WelcomeState initialized")
    
    def on_enter(self):
        """
        Function executed when the state is entered.
        It sets up the alarm, retrieves the weather forecast, and informs the user about their schedule.
        """
        logger.info("WelcomeState entered")
        
        # Calculate wake-up time based on the first calendar appointment
        wakeup_time = self.calc_alarm_time()
        logger.info(f"Wake-up time set for: {wakeup_time}")

        # TODO: Set the alarm using the calculated wakeup_time

        # Retrieve and provide the current weather forecast
        weather_forecast = self.weather_api.get_daily_forecast("Stuttgart", datetime.datetime.today()) # Using tomorrow's date
        min_temp = weather_forecast.get('min_temp', None)
        max_temp = weather_forecast.get('max_temp', None)
        condition = weather_forecast.get('avg_condition', None)
        
        current_weather = self.weather_api.get_weather("Stuttgart")
        
        # Build a string with the populated elements and provide the user with the information
        good_morning_message = f"Guten Morgen! Es ist {datetime.datetime.now().strftime('%H:%M')}. "
        
        weather_info = ""
        if min_temp is not None and max_temp is not None:
            weather_info = f"Die Wettervorhersage für heute: Die Temperatur wird zwischen {int(min_temp)}°C und {int(max_temp)}°C liegen."
            if condition is not None:
                # remove lst character from condition string
                weather_info = weather_info[:-1]
                weather_info += f" und es wird {condition.lower()}."
        
        if current_weather:
            current_weather_info = f" Im Moment sind es {int(current_weather['main']['temp'])}°C."
        else:
            current_weather_info = ""
            
        print(good_morning_message + weather_info + current_weather_info)
        self.tts_api.speak(good_morning_message + weather_info + current_weather_info)
        
        # TODO: Check for delays in the public transport
        
        # Provide the user with the information about their first appointment
        appointments = self.rapla_api.get_todays_appointments()
        if appointments:
            first_appointment = appointments[0]
            self.tts_api.speak(f" Ihr erster Termin ist um {first_appointment.start} in {first_appointment.room}.")
        else:
            self.tts_api.speak("Sie haben heute keine Termine.")
        
        # Ask the user if they want to start the next use case (e.g., Nachrichtenassistent)
        user_response = self.tts_api.ask_yes_no("Möchten Sie die Nachrichten hören?")
        if user_response:
            self.state_machine.morning_news()
        else:
            self.tts_api.speak("Okay, lassen Sie mich wissen wenn ich Ihnen helfen kann!")
            self.state_machine.interaction()
        
    def calc_alarm_time(self):
        """
        Calculate the time for the alarm clock based on the first appointment of the user's calendar.
        """
        
        # Retrieve user's calendar entries for the next day 
        calendar_entries = self.rapla_api.get_todays_appointments()
        
        if not calendar_entries:
            return self.default_wakeup_time
        
        first_appointment = calendar_entries[0]        
        

        # Route to the appointment location is determined using the navigation service (address from preferences file) 
        # ...
        # ...
        transit_time = 30 # result of the routing service
     
        # Calculate required time for alarm clock 
        first_appointment_time = datetime.datetime.strptime(first_appointment.start, "%H:%M").time()
        first_appointment_date = datetime.datetime.strptime(first_appointment.date, "%d.%m.%Y")
        first_appointment_datetime = datetime.datetime.combine(first_appointment_date, first_appointment_time)
        
        # Check second alternative process and set latest alarm time to be no later than default_wakeup_time        
        if first_appointment_time > self.default_wakeup_time:
            return self.default_wakeup_time
        
        alarm_time = first_appointment_datetime - datetime.timedelta(minutes=transit_time)
        return alarm_time.time()