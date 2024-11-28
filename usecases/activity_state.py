import datetime

from loguru import logger
from api.fitbit_api.main import FitbitAPI  
import pandas as pd
from api.spotify_api.main import SpotifyAPI


class ActivityState:
    """
    State that represents the activity/health use case.
    """

    def __init__(self, state_machine):
        """
        Initializes the ActivityState object.

        Args:
            state_machine: The state machine object.
        """
        self.running = True
        self.state_machine = state_machine
        
        self.fitbit_api= self.state_machine.api_factory.create_api(api_type="fitbit")
        self.tts_api = self.state_machine.api_factory.create_api(api_type="tts")
        self.spotify_api = self.state_machine.api_factory.create_api(api_type="spotify") 
        logger.info("ActivityState initialized")

    def on_enter(self):
        """
        Function executed when the state is entered.
        It calculates the stress level and logs actions based on the result.
        """
        logger.info("ActivityState entered")
        
        # Berechnung des Stresslevels
        stress_level = self.calculate_daily_stress_level(date=str(datetime.date.today()))
        logger.debug(f"Calculated stress level: {stress_level}")
        
        if stress_level is not None:
            # TTS deaktiviert
            # self.tts_api.speak(f"Dein Stresslevel ist {stress_level} von 100.")
            logger.info(f"Dein Stresslevel ist {stress_level} von 100.")
            
            logger.debug("About to suggest music based on stress level.")
            self.suggest_music(stress_level)
        else:
            # TTS deaktiviert
            # self.tts_api.speak("Es tut mir leid, ich konnte dein Stresslevel nicht messen.")
            logger.error("Stress level calculation failed.")

        logger.debug("Exiting ActivityState.")
        self.state_machine.transition_to_idle()  # Zurück in den Idle-Zustand

    def calculate_daily_stress_level(self, date: str) -> str:
        """
        Calculates the stress category (very relaxed, normal, stress) 
        based on the average heart rate during inactive phases.

        Args:
            date (str): The date for which the data should be analyzed (in 'YYYY-MM-DD' format).

        Returns:
            str: The stress category ('sehr entspannt', 'normal', 'stress'), or None if calculation fails.
        """
        try:
            # Fetch heart rate and steps data
            heart_data = self.fitbit_api.get_heart_data(date)
            steps_data = self.fitbit_api.get_steps_data(date)

            # Process data
            records = []
            step_data = {step['time']: step['value'] for step in steps_data['activities-steps-intraday']['dataset']}

            for heart_point in heart_data['activities-heart-intraday']['dataset']:
                heart_time = heart_point['time']
                heart_rate = heart_point['value']
                step_count = step_data.get(heart_time, 0)

                # Determine activity phase based on step count
                phase = 'Inactive' if step_count < 60 else 'Active'

                # Add entry to records
                records.append({
                    'Time': heart_time,
                    'Heart Rate': heart_rate,
                    'Steps': step_count,
                    'Phase': phase
                })

            # Create DataFrame
            df = pd.DataFrame(records)

            # Calculate average heart rate during inactive phases
            inactive_rates = df[df['Phase'] == 'Inactive']['Heart Rate']
            if not inactive_rates.empty:
                average_heart_rate = inactive_rates.mean()
                logger.debug(f"Average heart rate during inactive phases: {average_heart_rate:.2f} bpm")

                # Categorize stress level
                if average_heart_rate < 60:
                    return "sehr entspannt"  # Very relaxed
                elif 60 <= average_heart_rate <= 75:
                    return "normal"  # Normal
                else:
                    return "stress"  # Stress

            logger.warning("Keine inaktiven Phasen gefunden.")
            return None

        except Exception as e:
            logger.error(f"Error calculating stress level: {e}")
            return None

    def suggest_music(self, stress_category):
        """
        Suggests and logs actions based on the stress category.

        Args:
            stress_category (str): The calculated stress category ('sehr entspannt', 'normal', 'stress').
        """
        # Playlist-IDs für jeden Mood
        playlist_map = {
            "sehr entspannt": "37i9dQZF1DWZd79rJ6a7lp",  # Example: Relaxing playlist
            "normal": "37i9dQZF1DX4sWSpwq3LiO",        # Example: Calm playlist
            "stress": "37i9dQZF1DX9XIFQuFvzM4"         # Example: Happy playlist
        }

        # Playlist-ID basierend auf dem Mood auswählen
        playlist_id = playlist_map.get(stress_category)
        if not playlist_id:
            # self.tts_api.speak("Es tut mir leid, ich konnte keine passende Playlist finden.")
            logger.error(f"No playlist found for stress category: {stress_category}")
            return

        # TTS deaktiviert
        mood_text = {
            "sehr entspannt": "entspannende Musik",
            "normal": "ruhige Musik",
            "stress": "fröhliche Musik"
        }.get(stress_category, "ruhige Musik")

        # self.tts_api.speak(f"Ich werde {mood_text} für dich abspielen.")
        logger.info(f"Attempting to play playlist {playlist_id} for mood: {stress_category}")

        try:
            # Geräte abrufen und das erste verfügbare Gerät verwenden
            devices = self.spotify_api.get_available_devices()
            if not devices:
                raise Exception("No available devices for playback.")
            
            active_device = devices[0]  # Wähle das erste verfügbare Gerät
            device_id = active_device['id']

            # Log Wiedergabe
            logger.info(f"Would start playback of playlist {playlist_id} on device {device_id} (mocked).")
            # self.spotify_api.start_playback(playlist_id=playlist_id, device_id=device_id)
            logger.info(f"Playback of playlist {playlist_id} successfully logged.")

        except Exception as e:
            logger.error(f"Error playing music: {e}")
            # self.tts_api.speak("Es gab ein Problem beim Abspielen der Musik.")

    def on_exit(self):
        """
        Cleans up resources or actions when exiting the state.
        """
        logger.info("Exiting ActivityState.")
        # self.music_api.stop()  # Stop any playing music


# if __name__ == "__main__":
#     class MockStateMachine:
#         def transition_to_idle(self):
#             logger.info("Transitioning to idle state.")

#     state_machine = MockStateMachine()
#     activity_state = ActivityState(state_machine)
#     activity_state.on_enter()
