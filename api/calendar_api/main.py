from typing import Dict
from urllib.parse import quote
from api.api_client import APIClient
from .rapla import Calendar, create_calendar_from_rapla


class RaplaAPI(APIClient):
    """
    API client for accessing rapla from a given url.
    """
    calendar: Calendar = None
    url: str = None

    def __init__(self, start_year: int, class_letter: str, email: str = 'doelker@verwaltung.ba-stuttgart.de'):
        """
        Initializes the API client with the given Year and Class.
        Optional email to restrict view to permissions of viewer
        
        :param start_year: Start year of the class to get the Calendar from.        
        :param class_letter: Which class in the year should be selected.
        :param email: Email of the user accessing the calendar (Optional).
        """
        encoded_email = quote(email)
        encoded_start_year = quote(str(start_year))
        encoded_class_letter = quote(class_letter)
        
        self.url = f"https://rapla.dhbw.de/rapla/internal_calendar?user={encoded_email}&file={encoded_start_year}{encoded_class_letter}&day=30&month=9&year=2024&pages=20"
        super().__init__(self.url)
        
        if not self.calendar:
            self.update_rapla_calendar()
            
    def authenticate(self):
        """
        Rapla is open and doesnt need auth.
        """
        pass

    def update_rapla_calendar(self):
        """
        Updates the rapla calendar with the url.
        """
        self.calendar = create_calendar_from_rapla(self.url)


if __name__ == '__main__':
    for letter in ['A']:  # ['A', 'B', 'C', 'D', 'E', 'F']
        url = f"https://rapla.dhbw.de/rapla/internal_calendar?user=doelker%40verwaltung.ba-stuttgart.de&file=22{letter}&day=30&month=9&year=2024&pages=20"
        cal = create_calendar_from_rapla(url)
        cal.save(f"calendar_inf22{letter}.json")