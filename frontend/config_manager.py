import json
import os

class ConfigManager:
    
    def __init__(self, view):
        """Initialize the ConfigManager.

        Args:
            view: An instance of the view class that contains the UI components.
        """

        self.view = view
        self.ui = self.view.ui
        self.preferences_file = '../config/preferences.json'
        self.preferences = self.load_preferences()

    def load_preferences(self):
        """Load preferences from a JSON file.

        If the preferences file does not exist, return an empty dictionary.

        Returns:
            dict: A dictionary containing the loaded preferences.
        """

        if os.path.exists(self.preferences_file):
            with open(self.preferences_file, 'r') as file:
                return json.load(file)
        return {}

    def save_preferences(self):
        """Save the current preferences to a JSON file.

        This method writes the preferences dictionary to the specified JSON file.
        """

        with open(self.preferences_file, 'w') as file:
            json.dump(self.preferences, file, indent=4)

    def get_fuel_type(self):
        """Return the fuel type from preferences.

        If the fuel type is not set, return None.

        Returns:
            str or None: The stored fuel type, or None if not set.
        """

        return self.preferences.get('fuel_type', None)

    def set_fuel_type(self, selected_data):
        """Update the fuel type based on the selected data.

        Args:
            selected_data (str): The data selected in the combo box representing the fuel type.
        """

        self.preferences['fuel_type'] = selected_data
        self.save_preferences()
        print(f'Updated fuel_type: {self.get_fuel_type()}')

