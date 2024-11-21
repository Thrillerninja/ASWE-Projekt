import json
import os
from PyQt5.QtCore import QTime
from typing import Union

class ConfigManager:
    
    def __init__(self, view):
        """Initialize the ConfigManager.

        Args:
            view: An instance of the view class that contains the UI components.
        """

        self.view = view
        self.ui = self.view.ui

        script_dir = os.path.dirname(os.path.realpath(__file__))
        parent_dir = os.path.dirname(script_dir)  # Go up one directory
        self.preferences_file = os.path.join(parent_dir, 'config', 'preferences.json')

        self.preferences = {}
        self.fuel_types = ['super-e10', 'super-e5', 'super-plus', 'diesel', 'lkw-diesel', 'lpg',]

        self.load_preferences_file()
        self.set_initial_values()

    def load_preferences_file(self) -> None:
        """Loads preferences from a JSON file into the `self.preferences` dictionary.

        If the file does not exist or is empty, `self.preferences` will remain an empty dictionary.
        """
        try:
            with open(self.preferences_file, 'r') as file:
                self.preferences = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.preferences = {}

    def save_preferences(self) -> None:
        """Saves the current preferences from `self.preferences` to a JSON file.

        This will overwrite the file specified in `self.preferences_file`.
        """
        with open(self.preferences_file, 'w') as file:
            json.dump(self.preferences, file, indent=4)

    def update_preference(self, preference: str, data: Union[str, float]) -> None:
        """Updates or adds a preference in `self.preferences`.

        Args:
            preference (str): The name of the preference to update.
            data (Union[str, float]): The value to assign to the preference.
        """
        self.preferences[preference] = data
        # print(f'preference updated with value: {self.preferences[preference]}')

    def get_preference(self, preference: str) -> Union[str, float, None]:
        """Retrieves the value of a given preference.

        Args:
            preference (str): The name of the preference to retrieve. The available keys are:
                - "fuel_type": str (e.g., "diesel")
                - "fuel_threshold": float in € (e.g., 1.5)
                - "fuel_step_size": float in € (e.g., 0.05)
                - "fuel_radius": float in km (e.g., 5.0)
                - "fuel_demo_price": float in €, 0 indicates to use the API
                - "default_alarm_time": str (e.g., "08:00")
                - "sleep_time": str (e.g., "22:00")
                - "home_location": dict (see below for details)
                - "default_destination": dict (see below for details)

        Returns:
            Union[str, float, None]: The value of the preference if it exists, otherwise `None`.

        The dictionary for "home_location" and "default_destination" contain the following keys:
            - "name": str (e.g., "asperg")
            - "vvs_code": str (e.g., "de:08118:7400")
            - "address": dict, containing:
                - "street": str (e.g., "Alleenstraße")
                - "number": str (e.g., "1")
                - "zipcode": str (e.g., "71679")
                - "city": str (e.g., "Asperg")
                - "country": str (e.g., "Germany")
            - "coordinates": dict, containing:
                - "latitude": float (e.g., 48.907256)
                - "longitude": float (e.g., 9.147977)
        """
        return self.preferences.get(preference)
    
    def set_initial_values(self) -> None:
        """Sets the initial values for the UI elements from preferences.

        This method initializes the combo box for fuel type, sets the times for the alarm 
        and sleep, and configures the fuel threshold slider and line edit based on stored preferences.
        """
        fuel_type = self.preferences['fuel_type']
        for i, typ in enumerate(self.fuel_types):
            if fuel_type == typ:
                self.view.set_cb_fuel_type(i)
                break
                
        default_alarm_time = QTime.fromString(self.preferences['default_alarm_time'], "hh:mm")
        sleep_time = QTime.fromString(self.preferences['sleep_time'], "hh:mm")
        self.view.set_te_default_alarm_time(default_alarm_time)
        self.view.set_te_sleep_time(sleep_time)

        fuel_threshold = self.preferences['fuel_threshold']
        self.view.set_sl_fuel_threshold(int(fuel_threshold * 100))
        self.view.set_le_fuel_threshold(f"{fuel_threshold:.2f}")

        self.view.set_le_fuel_demo_price(f"{self.preferences['fuel_demo_price']:.2f}")

    def on_cb_fuel_type_changed(self, index: int) -> None:
        """Handles the change in the fuel type selection from the combo box.

        Args:
            index (int): The index of the selected fuel type in the combo box.

        Updates the `fuel_type` preference based on the selected fuel type index.
        """
        selected_fuel_type = self.fuel_types[index]
        self.update_preference('fuel_type', selected_fuel_type)

    def on_time_changed(self, key: str, time: QTime) -> None:
        """Handles the change in time (e.g., alarm time or sleep time).

        Args:
            key (str): The preference key related to the time being changed.
            time (QTime): The new time value.

        Updates the specified time preference with the new `QTime`.
        """
        time_string = time.toString("HH:mm")
        self.update_preference(key, time_string)

    def on_sl_fuel_threshold_changed(self, value: int) -> None:
        """Handles the change in the fuel threshold slider.

        Args:
            value (int): The new value from the fuel threshold slider, which is between 100 and 200.

        Divides the slider value by 100 and updates the `fuel_threshold` preference.
        Also updates the label display for the fuel threshold.
        """
        # Convert the slider value to a float (e.g., 150 becomes 1.50)
        fuel_threshold = value / 100.0
        fuel_threshold_str = f"{fuel_threshold:.2f}"
        
        self.update_preference('fuel_threshold', fuel_threshold)
        self.view.set_le_fuel_threshold(fuel_threshold_str)

    def convert_text_to_float(self, text: str):
        """Attempts to convert the text to a float, handling both comma and dot notation for decimal points.
        If the conversion fails, -1 is returned.

        Args:
            text (str): The text to convert to float.
        """
        text = text.strip()  # Remove any leading or trailing whitespace
        if text.endswith(" €"):
            text = text[:-2].strip()
        try:
            value = float(text.replace(",", "."))
            return value
        except ValueError:
            # conversion to float fails
            return -1
        
    def on_le_fuel_threshold_changed(self, text: str) -> None:
        """Handles the change in the fuel threshold input field.

        Args:
            text (str): The text from the input field representing the fuel threshold.

        Attempts to convert the text to a float, handling both comma and dot notation for decimal points.
        If successful, updates the `fuel_threshold` preference and slider. If not, calls an error function.
        """
        self.view.remove_error_le_fuel_threshold()
        value = self.convert_text_to_float(text)

        if 100 <= value * 100 <= 200:
            self.update_preference('fuel_threshold', value)
            self.view.set_sl_fuel_threshold(int(value * 100))
            self.view.set_le_fuel_threshold(f"{value:.2f}")
        else:
            self.view.show_error_le_fuel_threshold("Fuel threshold must be a number between 1.00 and 2.00")


    def on_le_fuel_demo_price_changed(self, text: str) -> None:
        """Handles the change in the fuel demo price input field.

        Args:
            text (str): The text from the input field representing the fuel demo price.

        Attempts to convert the text to a float, handling both comma and dot notation for decimal points.
        If conversion to float is successful, updates the `fuel_demo_price` preference and slider. If not, calls an error function.
        """

        self.view.remove_error_le_fuel_threshold()
        value = self.convert_text_to_float(text)

        if value >= 0:
            self.update_preference('fuel_demo_price', value)
            self.view.set_le_fuel_demo_price(f"{value:.2f}")
        else:
            self.view.show_error_le_fuel_threshold("Fuel threshold must be a number")