import datetime
import json
from typing import Dict, List
from api.api_client import APIClient
from . import rapla


class RaplaAPI(APIClient):
    """
    API client for accessing rapla from a given url.
    """

    def __init__(self, url: str, calendar:rapla.Calendar=None):
        """
        Initializes the API client with the given URL and calendar.
        """
        self.url:str = url
        self.calendar:rapla.Calendar = calendar
        if not calendar: self.update_rapla_calendar()
        
    def authenticate(self):
        """
        Authentication is not required for accessing rapla.
        """
        pass

    def update_rapla_calendar(self):
        """
        Updates the rapla calendar with the url.
        """
        self.calendar = rapla.create_calendar_from_rapla(self.url)

    def get_todays_appointments(self) -> List[rapla.Appointment]:
        """
        Returns the appointments for today.
        """
        today = datetime.datetime.now().strftime("%d.%m.%Y")
        return [appt for appt in self.calendar.appointments if appt.date == today]

    def get_appointments_for_date(self, date: str) -> List[rapla.Appointment]:
        """
        Returns the appointments for a specific date in the format DD.MM.YYYY.
        """
        return [appt for appt in self.calendar.appointments if appt.date == date]

    def get_calendar_as_json(self) -> str:
        """
        Returns the entire calendar in JSON format.
        """
        return json.dumps(self.calendar.to_json(), indent=4, ensure_ascii=False)

    def save_calendar_to_file(self, filepath: str):
        """
        Saves the current calendar to a specified JSON file.
        """
        self.calendar.save(filepath)

    def refresh_calendar(self):
        """
        Refreshes the calendar data by fetching it again from the URL.
        """
        self.calendar = self.update_rapla_calendar()



if __name__ == '__main__':
    for letter in ['A']:  # ['A', 'B', 'C', 'D', 'E', 'F']
        url = f"https://rapla.dhbw.de/rapla/internal_calendar?user=doelker%40verwaltung.ba-stuttgart.de&file=22{letter}&day=30&month=9&year=2024&pages=20"
        cal = rapla.create_calendar_from_rapla(url)
        cal.save(f"calendar_inf22{letter}.json")