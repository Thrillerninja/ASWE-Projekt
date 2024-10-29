import os
import pandas as pd
import requests
from fitbit_api import FitbitAPI

class FitbitDataProcessor:
    def __init__(self):
        self.fitbit_api = FitbitAPI()

    def calculate_daily_stress_level(self, date: str) -> pd.DataFrame:
        """
        Calculates the daily stress level based on heart rate and step count data.
        
        This method fetches heart rate and step count data for the specified date,
        analyzes the data, categorizes the phases as 'Active' or 'Inactive' based on
        the step count, and calculates the average heart rate during inactive phases.
        Finally, the results are saved to a CSV file, and a DataFrame is returned.

        :param date: The date for which the data should be analyzed (in 'YYYY-MM-DD' format).
        :return: A DataFrame containing heart rate, step count, and phase information.
        """
        try:
            # Fetch heart and steps data
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
                phase = 'Inactive' if step_count < 75 else 'Active'

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
                average_stress_level = inactive_rates.mean()
                stress_category = self.categorize_stress_level(average_stress_level)

                print(f"Durchschnittliches Stresslevel: {average_stress_level:.2f} bpm - Kategorie: {stress_category}")
            else:
                print("Keine inaktiven Phasen gefunden.")

            # Ensure the 'data' directory exists in the current working directory
            current_directory = os.path.dirname(os.path.abspath(__file__))  # Aktuelles Verzeichnis der Python-Datei
            data_directory = os.path.join(current_directory, 'data')  # 'data'-Ordner im aktuellen Verzeichnis
            os.makedirs(data_directory, exist_ok=True)  # Ordner erstellen, falls nicht vorhanden

            # Save DataFrame to CSV in the 'data' directory
            csv_file_path = os.path.join(data_directory, f'stress_data_{date}.csv')
            df.to_csv(csv_file_path, index=False)
            print(f"File {csv_file_path} successfully saved.")

            return df

        except requests.RequestException as e:
            print("Error fetching or parsing data:", e)
            return pd.DataFrame()  # Return empty DataFrame on error

    def categorize_stress_level(self, average_heart_rate: float) -> str:
        """
        Categorizes the stress level based on the average heart rate.
        """
        if 60 <= average_heart_rate <= 80:
            return "Normal"
        elif average_heart_rate > 80:
            return "Stress"
        else:
            return "Ungültiger Wert"  # Falls die Herzfrequenz unrealistisch niedrig ist
