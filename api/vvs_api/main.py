from typing import List
from vvspy.enums import Station
from vvspy import get_trip
from rapidfuzz import process, fuzz

from search import search_stations_by_name

class VVSAPI():
    """
    API client for accessing public transportation data.
    """

    def __init__(self):
        pass
    
    def authenticate(self):
        """
        No authentication steps are required.
        """
        pass

    def normalize_input(self, input_str: str) -> str:
        """
        Normalize the user input by replacing spaces with underscores and converting to uppercase.
        
        :param input_str: User input string to normalize.
        :return: Normalized string.
        """
        return '_'.join(input_str.strip().upper().split())

    def check_user_station_search_offline(self, user_input: str) -> List[Station]:
        """
        Uses fuzzy matching to check if the user input matches a station name.
        
        :param user_input: User input to check.
        :return: List of stations that match the user input.
        """
        # Normalize user input to match enum formatting (e.g., 'SÜDHEIMER_PLATZ_3')
        normalized_input = self.normalize_input(user_input)

        # Assuming `Station` enum contains a list of station names in the format 'SÜDHEIMER_PLATZ_3'
        station_names = {station.name: station for station in Station}

        # First check if normalized input is an exact match
        if normalized_input in station_names:
            return [station_names[normalized_input]]

        # Perform fuzzy matching (using token_sort_ratio for better results)
        station_name_list = list(station_names.keys())
        matches = process.extract(normalized_input, station_name_list, 
                                  scorer=fuzz.token_sort_ratio, limit=5, score_cutoff=70)
        
        # Convert matched station names back to Station enum instances
        matched_stations = [station_names[station[0]] for station in matches]
        
        return matched_stations

    def calc_trip_time(self, start_station: Station, end_station: Station) -> int:
        """
        Calculate the trip time between two stations.
        
        :param start_station: Starting station.
        :param end_station: Ending station.
        :return: Estimated trip time in minutes.
        """
        # Check if the trip time between the two stations exists
        trip_time = get_trip(start_station, end_station)
        
        # If not found, check the reverse direction (for bidirectional trips)
        if trip_time is None:
            trip_time = get_trip(end_station, start_station)
        
        return trip_time
    
    def search_station_name(self, station_name: str, type: str) -> List[Station]:
        """
        Search for a station by name.
        
        :param station_name: Name of the station to search for.
        :return: List of matching Station objects.
        """
        stations = search_stations_by_name(station_name)
        
        stations = [station for station in stations if station.type == type]
        
        return stations

# Example usage
obj = VVSAPI()

# Searching for stations
start_station = obj.check_user_station_search_offline('stuttgart_stadtmitte')[0]
end_station = obj.check_user_station_search_offline('HÜLBEN_NORD')[0]

# Calculate trip time
trip_time = obj.calc_trip_time(start_station, end_station)
print(f"Trip time from {start_station} to {end_station}: {trip_time} minutes")

stations = obj.search_station_name('holz', "stop")
for station in stations:
    station.info()