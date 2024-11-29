import datetime
import os
from loguru import logger
from typing import Optional
from api.fitbit_api.main import FitbitAPI
import pandas as pd
from api.spotify_api.main import SpotifyAPI

class ActivityState:
    """
    Represents the activity/health use case.
    """

    def __init__(self, state_machine):
        # Initialize the state and required APIs
        self.running = True
        self.state_machine = state_machine
        self.fitbit_api = self.state_machine.api_factory.create_api(api_type="fitbit")
        self.tts_api = self.state_machine.api_factory.create_api(api_type="tts")
        self.spotify_api = self.state_machine.api_factory.create_api(api_type="spotify")
        self.last_activated_at = datetime.datetime.min.strftime('%Y-%m-%d %H:%M')
        self.last_playback_stop_activated_at = datetime.datetime.min.strftime('%Y-%m-%d %H:%M')
        logger.info("ActivityState initialized")

    def on_enter(self):
        # Entry point for the activity state
        logger.info("ActivityState entered")
        
        date = str(datetime.date.today())
        self.last_activated_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        
        # Calculate the user's stress level based on Fitbit data
        stress_level = self.calculate_daily_stress_level(date)
        logger.debug(f"Calculated stress level: {stress_level}")
        
        if stress_level:
            # Fetch resting heart rate data for additional feedback
            resting_heart_rate = self.fitbit_api.get_heart_data(date)['activities-heart'][0]['value']['restingHeartRate']
            self.tts_api.speak(
                f"Dein Stresslevel wurde heute anhand deiner Herzfrequenz und Aktivitätsdaten analysiert. "
                f"Deine Ruheherzfrequenz betrug {resting_heart_rate} Schläge pro Minute."
            )
            logger.info(f"Stress level: {stress_level}")
            
            # Suggest music based on the stress level
            self.suggest_music(stress_level)
        else:
            self.tts_api.speak("Entschuldigung, ich konnte dein Stresslevel nicht messen.")
            logger.error("Stress level calculation failed.")

        # Analyze and provide feedback on sleep data for the last 'days' days
        days = 2
        avg_sleep_time = self.average_sleep_time(days)
        if avg_sleep_time:
            self.tts_api.speak(f"Deine durchschnittliche Schlafzeit der letzten {days} Tage beträgt {avg_sleep_time}.")
        else:
            self.tts_api.speak(f"Entschuldigung, ich konnte keine Schlafdaten der letzten {days} Tage finden.")

        logger.debug("Exiting ActivityState.")
        
        # Transition back to an idle state
        self.state_machine.activity_idle()

    def calculate_daily_stress_level(self, date: str) -> Optional[str]:
        """
        Calculate the user's daily stress level based on Fitbit heart and step data.
        """
        try:
            # Fetch heart rate and step data from Fitbit API
            heart_data = self.fitbit_api.get_heart_data(date)
            steps_data = self.fitbit_api.get_steps_data(date)
            resting_heart_rate = heart_data['activities-heart'][0]['value']['restingHeartRate']
            logger.debug(f"Resting Heart Rate: {resting_heart_rate} bpm")

            # Combine heart rate data with step count for context
            records = []
            step_data = {step['time']: step['value'] for step in steps_data['activities-steps-intraday']['dataset']}

            for heart_point in heart_data['activities-heart-intraday']['dataset']:
                heart_time = heart_point['time']
                heart_rate = heart_point['value']
                step_count = step_data.get(heart_time, 0)
                phase = 'Inactive' if step_count < 60 else 'Active'
                records.append({'Time': heart_time, 'Heart Rate': heart_rate, 'Steps': step_count, 'Phase': phase})

            # Save processed data to a CSV file for further analysis or debugging
            df = pd.DataFrame(records)
            project_dir = os.path.dirname(os.path.abspath(__file__))
            output_dir = os.path.join(project_dir, "..", "api", "fitbit_api", "data")            
            os.makedirs(output_dir, exist_ok=True) 
            output_file = os.path.join(output_dir, f"activity_data_{date}.csv")
            df.to_csv(output_file, index=False)
            logger.info(f"Activity data saved to {output_file}")
            
            # Analyze inactive phases to determine stress level
            inactive_rates = df[df['Phase'] == 'Inactive']['Heart Rate']
            if not inactive_rates.empty:
                average_heart_rate = inactive_rates.mean()
                logger.debug(f"Average heart rate during inactive phases: {average_heart_rate:.2f} bpm")

                if average_heart_rate < resting_heart_rate - 10:
                    return "sehr entspannt"
                elif resting_heart_rate - 10 <= average_heart_rate <= resting_heart_rate + 10:
                    return "entspannt"
                else:
                    return "gestresst"

            # Log warning if no inactive phases are detected
            logger.warning("No inactive phases found.")
            return None
        except Exception as e:
            # Handle and log any errors during data processing
            logger.error(f"Error calculating stress level: {e}")
            return None

    def suggest_music(self, stress_category):
        """
        Suggest music based on stress category and optionally play it.
        """
        # Map stress categories to Spotify playlists
        playlist_map = {
            "sehr entspannt": "37i9dQZF1DWZd79rJ6a7lp", # TODO replace with actual playlist IDs
            "entspannt": "37i9dQZF1DX4sWSpwq3LiO",
            "gestresst": "37i9dQZF1DX9XIFQuFvzM4"
        }
        playlist_id = playlist_map.get(stress_category)
        if not playlist_id:
            self.tts_api.speak("Entschuldigung, ich konnte keine passende Playlist finden.")
            logger.error(f"No playlist found for stress category: {stress_category}")
            return

        # Provide a recommendation message based on the stress level
        recommendations = {
            "sehr entspannt": "Du warst heute sehr entspannt. Wie wäre es mit Musik, um diese Stimmung zu halten?",
            "entspannt": "Du warst heute in einem guten, entspannten Zustand. Musik könnte den Abend noch besser machen.",
            "gestresst": "Du scheinst heute gestresst gewesen zu sein. Entspannende Musik könnte helfen, vor dem Schlafen abzuschalten."
        }

        self.tts_api.speak(recommendations.get(stress_category, ""))
        
        # Ask the user if they want to play the recommended playlist
        user_response = self.tts_api.ask_yes_no("Möchtest du die Musik abspielen?")
        if user_response:
            try:
                # Use Spotify API to start music playback on a specific device
                logger.info(f"Would start playback of playlist {playlist_id}.")
                self.spotify_api.start_playback(playlist_id=playlist_id)
                logger.info(f"Playback of playlist {playlist_id} successfully started.")
            except Exception as e:
                # Handle playback errors
                logger.error(f"Error playing music: {e}")
                self.tts_api.speak("Es gab ein Problem beim Abspielen der Musik.")
        else:
            self.tts_api.speak("Okay, gute Nacht!")


        
    def average_sleep_time(self, days=1): 
        """
        Calculates the average sleep start time over the last 'days' days.
        :param days: Number of days to calculate the average sleep start time for (including today).
        :return: The average sleep start time in 'HH:MM' format, or None if no data is available.
        """
        today = datetime.date.today()
        sleep_start_times = []

        for i in range(days):
            date = (today - datetime.timedelta(days=i)).strftime('%Y-%m-%d')
            sleep_start_time = self.get_sleep_start_time(date)

            if sleep_start_time:
                # Convert sleep start time into minutes since midnight
                try:
                    sleep_start = datetime.datetime.strptime(sleep_start_time, '%H:%M')
                    sleep_minutes = sleep_start.hour * 60 + sleep_start.minute
                    sleep_start_times.append(sleep_minutes)
                except ValueError:
                    logger.error(f"Error converting sleep start time for {date}: {sleep_start_time}")
                    continue

        if not sleep_start_times:
            logger.warning("No sleep start times found for the specified days.")
            return None

        # Calculate the average sleep start time (in minutes)
        avg_sleep_minutes = sum(sleep_start_times) / len(sleep_start_times)
        
        # Convert the average time back to hours and minutes
        avg_sleep_hours = int(avg_sleep_minutes // 60)
        avg_sleep_minutes = int(avg_sleep_minutes % 60)

        # Return the result in HH:MM format
        avg_sleep_time = f"{avg_sleep_hours:02}:{avg_sleep_minutes:02}"
        logger.info(f"Average sleep start time over the last {days} days: {avg_sleep_time}")
        return avg_sleep_time


    def get_sleep_start_time(self, date: str) -> Optional[str]:
        """
        Retrieves the user's sleep start time (primarily at night).
        :param date: The date for which to retrieve the sleep start time, in 'YYYY-MM-DD' format.
        :return: Sleep start time as a string, or None if no data is available.
        """
        try:
            # Fetch sleep data from the Fitbit API
            sleep_data = self.fitbit_api.get_sleep_data(date)
            
            if not sleep_data or 'sleep' not in sleep_data:
                logger.error(f"No sleep data found for date {date}")
                return None

            # Iterate through sleep periods to find the main sleep phase
            for sleep_period in sleep_data['sleep']:
                if sleep_period['isMainSleep']:
                    first_sleep_start_time = sleep_period['startTime']

                    sleep_start = datetime.datetime.strptime(first_sleep_start_time.split('.')[0], '%Y-%m-%dT%H:%M:%S')
                    
                    # Return the sleep start time in HH:MM format
                    sleep_start_time = sleep_start.strftime("%H:%M")
                    logger.info(f"User went to sleep at {sleep_start_time}.")
                    return sleep_start_time

            logger.warning(f"No main sleep phase found for date {date}.")
            return None

        except Exception as e:
            logger.error(f"Error retrieving sleep start time for {date}: {e}")
            return None
        
    def pause_spotify_playback(self):
        """Tries to stop spotify playback."""
        self.last_playback_stop_activated_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        try:
            self.spotify_api.pause_playback()
            logger.info("Spotify playback paused successfully.")
        except Exception as e:
            logger.warning(f"Error pausing Spotify playback: {e}")

    def get_one_hour_after_sleep_time(self, default_sleep_time: str) -> str:
        """Calculates the time that is exactly one hour after the given sleep time."""
        default_sleep_time_obj = datetime.datetime.strptime(default_sleep_time, '%H:%M')
        one_hour_after_sleep_time = (default_sleep_time_obj + datetime.timedelta(hours=1)).strftime('%H:%M')
        return one_hour_after_sleep_time


    def check_trigger_activity(self):
        #trigger Activity Use Case
        # calculated_sleep_time = self.average_sleep_time(days=2) 
        default_sleep_time = self.state_machine.preferences.get("sleep_time")

        current_day_and_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        current_time = current_day_and_time.split(" ")[1]

        one_hour_after_sleep_time = self.get_one_hour_after_sleep_time(default_sleep_time)

        if current_time == default_sleep_time and current_day_and_time != self.last_activated_at:
            self.state_machine.goto_activity()
        elif current_time == one_hour_after_sleep_time and current_day_and_time != self.last_playback_stop_activated_at:
            self.pause_spotify_playback()
