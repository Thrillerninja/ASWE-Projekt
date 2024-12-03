
import api.notification_api.win_push_notification as notifier
import api.petrol_api.main as petrol

import main


class PetrolChecker:

    def __init__(self):
        print("PetrolChecker initialized")
        city = main.sm.preferences['home_location']['name']
        fuel_name = main.sm.preferences['fuel_type']
        fuel_radius = int(main.sm.preferences['fuel_radius'])
        self.petrol_api = petrol.PetrolAPI(city=city,
                                           fuel_name=fuel_name,
                                           range_km=fuel_radius)
        self.notifier = notifier.PushNotifierAPI()
        self.notified = False
        self.last_notified_threshold = 0


    def start_check_loop(self):
        """
        Checks if the current petrol price is below the threshold in the preferences
        """
        while True:
            threshold_pref = main.sm.preferences['fuel_threshold']
            if not self.notified:
                self.last_notified_threshold = threshold_pref

            # Overwrite current price for demo purposes
            overwrite_current_price = float(main.sm.preferences['fuel_demo_price'])
            if overwrite_current_price > 0:
                current_price_eur = overwrite_current_price
            else:
                current_price_eur = self.petrol_api.get_current_lowest_price()

            # Reset notification flag if price is above threshold
            if self.notified and current_price_eur > threshold_pref:
                self.notified = False

            # Notify if price is below threshold
            if current_price_eur < self.last_notified_threshold:
                self.notified = True
                self.last_notified_threshold -= main.sm.preferences['fuel_step_size']  # Notify every x cents decrease 
                self.notifier.push(title="Spritpreis gesunken",
                                   message=f"Der aktuelle Preis beträgt {current_price_eur}€",
                                   duration=10,
                                   threaded=True)


