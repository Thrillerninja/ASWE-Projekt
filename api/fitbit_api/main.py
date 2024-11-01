from datetime import datetime
from fitbit_data import FitbitDataProcessor
from fitbit_auth import FitbitAuth

if __name__ == "__main__":
    # Example of how to call the functions

    # Uncomment the following two lines to perform the initial authentication -> This will create the 'fitbit_tokens.json' file
    fitbit_auth = FitbitAuth()
    #     fitbit_auth.authorize()

    # Note: Authentication only works with the application owner´s Fitbit account

    fitbit_data_processor = FitbitDataProcessor()
    today = datetime.now().strftime("%Y-%m-%d")
    fitbit_data_processor.calculate_daily_stress_level(today)
