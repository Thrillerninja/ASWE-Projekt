from typing import Dict

import rapla


class RaplaAPI():
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

    def update_rapla_calendar(self):
        """
        Updates the rapla calendar with the url.
        """
        self.calendar = rapla.create_calendar_from_rapla(url)





if __name__ == '__main__':
    for letter in ['A']:  # ['A', 'B', 'C', 'D', 'E', 'F']
        url = f"https://rapla.dhbw.de/rapla/internal_calendar?user=doelker%40verwaltung.ba-stuttgart.de&file=22{letter}&day=30&month=9&year=2024&pages=20"
        cal = rapla.create_calendar_from_rapla(url)
        cal.save(f"calendar_inf22{letter}.json")