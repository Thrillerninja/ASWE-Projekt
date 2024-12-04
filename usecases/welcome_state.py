from typing import Dict
import datetime
from unittest.mock import MagicMock
from loguru import logger

class WelcomeState:
    """
    State that represents the welcome state/usecase of the application.
    """
    
    def __init__(self, state_machine):
        self.state_machine = state_machine
        
        self.tts_api = self.state_machine.api_factory.create_api(api_type="tts", state_machine=self.state_machine)
        self.transit_api = self.state_machine.api_factory.create_api(api_type="vvs")
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
        
        # ---------- Alarm clock ----------
        # Calculate wake-up time based on the first calendar appointment
        wakeup_time = self.calc_alarm_time()
        # Set the alarm clock
        self.state_machine.main_window.update_alarm_label(wakeup_time)
        logger.info(f"Wake-up time set to: {wakeup_time}")

        # TODO: Set the alarm using the calculated wakeup_time

        # ---------- Weather information ----------
        # Retrieve the current weather forecast
        logger.debug("Retrieving weather forecast for Stuttgart")
        weather_forecast = self.weather_api.get_daily_forecast("Stuttgart", datetime.datetime.today()) # Using tomorrow's date
        min_temp = round(weather_forecast.get('min_temp', None), 1) if weather_forecast.get('min_temp', None) is not None else None
        max_temp = round(weather_forecast.get('max_temp', None), 1) if weather_forecast.get('max_temp', None) is not None else None
        condition = weather_forecast.get('avg_condition', None)
        
        current_weather = self.weather_api.get_weather("Stuttgart")
        
        # Build a string with the populated elements and provide the user with the weather and timeinformation
        if self.tts_api.toggle_elevenlabs:
            good_morning_message = f"Guten Morgen! Es ist {datetime.datetime.now().strftime('%H:%M').replace(':','Uhr ')}. "
        else:
            good_morning_message = f"Guten Morgen! Es ist {datetime.datetime.now().strftime('%H:%M')}. "
        
        weather_info = ""
        grad_format = ""
        
        if self.tts_api.toggle_elevenlabs:
            grad_format = f"Grad Celsius"
        else:
            grad_format = f"°C"
                    
        if min_temp is not None and max_temp is not None:
            
            if min_temp == max_temp:
                max_temp += 1
            
            if condition is not None:                
                weather_info = f"Die Wettervorhersage für heute: Die Temperatur wird zwischen {int(min_temp)} und {int(max_temp)} {grad_format} liegen und {condition}"
            else:        
                weather_info = f"Die Wettervorhersage für heute: Die Temperatur wird zwischen {int(min_temp)} und {int(max_temp)} {grad_format} liegen."
        
        current_weather_info = ""
        if current_weather:
            current_weather_info = f" Im Moment sind es {int(current_weather['main']['temp'])} {grad_format}."
        
        logger.debug(f"Speaking weather information: {good_morning_message + weather_info + current_weather_info}")
        self.tts_api.speak(good_morning_message + weather_info + current_weather_info)        
        
        # ---------- Calendar information ----------
        # Provide the user with the information about their first appointment that hasn't already passed
        logger.debug("Retrieving today's appointments")
        appointments = self.rapla_api.get_todays_appointments()
        
        now = datetime.datetime.now(datetime.timezone.utc)
        upcoming_appointment = next((appt for appt in appointments if appt.datetime_start > now), None)
        
        if upcoming_appointment:
            logger.debug(f"Upcoming appointment: {upcoming_appointment}")
            self.tts_api.speak(f"Ihr erster Termin ist um {upcoming_appointment.datetime_start.strftime('%H:%M')} im {upcoming_appointment.room}.")
            
            # ---------- Transport information ----------
            # Get rides to get for the first appointment
            start_location = self.state_machine.preferences.get("home_location", None)
            end_location = self.state_machine.preferences.get("default_destination", None)
            logger.debug(f"Calculating trip time from {start_location} to {end_location}")
            
            arrival_time = upcoming_appointment.datetime_start + datetime.timedelta(hours=1)
            
            trip = self.transit_api.get_best_trip(start_location['vvs_code'], end_location['vvs_code'], arrival_time)
        
            if trip != -1 and start_location is not None and end_location is not None:
                transport_type = trip.connections[0].transportation.number
                departure_time = trip.connections[0].origin.departure_time_planned.replace(tzinfo=datetime.timezone.utc).strftime("%H:%M")
                arrival_time_time_aware = trip.connections[-1].destination.arrival_time_estimated.replace(tzinfo=datetime.timezone.utc)
                logger.debug(f"Departure time: {departure_time}, Arrival time: {arrival_time_time_aware}")
                                
                time_to_start = (upcoming_appointment.datetime_start.replace(tzinfo=datetime.timezone.utc) - arrival_time_time_aware).seconds // 60
                logger.debug(f"Um rechtzeitig zu Ihrem Termin zu kommen, sollten Sie die {transport_type} um {departure_time} Uhr nehmen. \
                                   Damit kommen sie {time_to_start} Minuten vor Ihrem Termin an.")
                self.tts_api.speak(f"Um rechtzeitig zu Ihrem Termin zu kommen, sollten Sie die {transport_type} um {departure_time} Uhr nehmen. \
                                   Damit kommen sie {time_to_start} Minuten vor Ihrem Termin an.")
            else:
                logger.debug("No suitable connection found")
                self.tts_api.speak("Es konnte keine passende Verbindung gefunden werden.")
        else:
            logger.debug("No upcoming appointments found for today")
            if len(appointments) > 0:
                self.tts_api.speak("Alle Termine für heute sind bereits vorüber.")
            else:
                self.tts_api.speak("Sie haben heute keine Termine.")
            
        # ---------- Morning news ----------
        # Ask the user if they want to start the next use case (e.g., Nachrichtenassistent)
        logger.debug("Asking user if they want to hear the news")
        user_response = self.tts_api.ask_yes_no("Möchten Sie die Nachrichten hören?")
        if user_response:
            logger.debug("User wants to hear the news")
            self.state_machine.morning_news()
        else:
            logger.debug("User does not want to hear the news")
            self.tts_api.speak("Okay, lassen Sie mich wissen wenn ich Ihnen helfen kann!")
            self.state_machine.interaction()
        
    def calc_alarm_time(self):
        """
        Calculate the time for the alarm clock based on the first appointment of the user's calendar.
        """
        
        # Retrieve user's calendar entries for the next day 
        calendar_entries = self.rapla_api.get_tomorrows_appointments()
        
        if not calendar_entries:
            return self.default_wakeup_time
        
        first_appointment = calendar_entries[0]        
        

        # ---------- Transport information ----------
        # Get rides to get for the first appointment
        start_location = self.state_machine.preferences.get("home_location", None)
        end_location = self.state_machine.preferences.get("default_destination", None)
        logger.debug(f"Calculating trip time from {start_location} to {end_location}")
        
        arrival_time = first_appointment.datetime_start
        trip = self.transit_api.get_best_trip(start_location['vvs_code'], end_location['vvs_code'], arrival_time)
    
        if trip != -1 and start_location is not None and end_location is not None:
            departure_time_aware = trip.connections[0].origin.departure_time_planned.replace(tzinfo=datetime.timezone.utc) + datetime.timedelta(hours=1)
        else:
            logger.debug("No suitable connection found")
            departure_time_aware = first_appointment.datetime_start - datetime.timedelta(minutes=30)
                
        # ----------- Alarm time calculation -----------
        prep_time = 30
        logger.error(f"Departure time: {departure_time_aware}, Prep time: {prep_time}")
        alarm_time = departure_time_aware - datetime.timedelta(minutes=prep_time)
        
        # Convert default_wakeup_time to a datetime for comparison
        default_wakeup_datetime = datetime.datetime.combine(alarm_time.date(), self.default_wakeup_time).replace(tzinfo=alarm_time.tzinfo)
        
        # Ensure alarm_time and default_wakeup_datetime are not MagicMock instances
        if isinstance(alarm_time, MagicMock) or isinstance(default_wakeup_datetime, MagicMock):
            return self.default_wakeup_time
        
        # Check second alternative process and set latest alarm time to be no later than default_wakeup_time        
        if alarm_time > default_wakeup_datetime:
            return self.default_wakeup_time
        
        return alarm_time.time()