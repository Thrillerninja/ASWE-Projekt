
import api.notification_api.win_push_notification as notifier
import api.petrol_api.main as petrol


class PetrolChecker:

    def __init__(self):
        print("PetrolChecker initialized")
        self.petrol_api = petrol.PetrolAPI(city='Stuttgart',  # TODO get from preferences
                                           fuel_name='super-e10',  # TODO get from preferences
                                           range_km=5)  # TODO get from preferences (oder der Einfachheit halber fix auf 5km)
        self.notifier = notifier.PushNotifierAPI()
        self.notified = False
        self.last_notified_threshold = 0


    def start_check_loop(self):
        """
        Checks if the current petrol price is below the threshold in the preferences
        """
        while True:
            threshold_pref = 1.50  # TODO get from preferences
            if not self.notified:
                self.last_notified_threshold = threshold_pref

            # Overwrite current price for demo purposes
            overwrite_current_price = ""  # TODO get from GUI Input field
            if overwrite_current_price:
                current_price_eur = float(overwrite_current_price)
            else:
                current_price_eur = self.petrol_api.get_current_lowest_price()

            # Reset notification flag if price is above threshold
            if self.notified and current_price_eur > threshold_pref:
                self.notified = False

            # Notify if price is below threshold
            if current_price_eur < self.last_notified_threshold:
                self.notified = True
                self.last_notified_threshold -= 0.05  # Notify every 5 cents decrease 
                self.notifier.push(title="Spritpreis gesunken",
                                   message=f"Der aktuelle Preis beträgt {current_price_eur}€",
                                   duration=10,
                                   threaded=True)


