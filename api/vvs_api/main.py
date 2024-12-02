import requests  # Add requests import
from typing import List
from vvspy.enums import Station
import vvspy
from vvspy.models import Trip
import logging
import datetime
from api.api_client import APIClient

from .stop import Stop, VSSStationType

# Import the get_trips function with added arrival flags
from .vvs_api_lib_fix import get_trips
# Replace the get_trips function in the vvspy module with the one with added arrival flags
vvspy.get_trips = get_trips

# Set logging level for comtypes to WARNING to reduce log spam
logging.getLogger('comtypes').setLevel(logging.WARNING)

class VVSAPI(APIClient):
    """
    API client for accessing public transportation data.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(VVSAPI, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """
        Initializes the VVSAPI client with the base URL.
        """
        super().__init__("https://www3.vvs.de/vvs/")
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.DEBUG)
    
    def authenticate(self):
        """
        No authentication is required for the VVS API.
        """
        pass
    
    def search_station(self, station_name: str, station_type: VSSStationType) -> List[Station]:
        """
        Search for stations by name and filter by station type.

        Args:
            station_name (str): Search string to get mathing stations.
            type (VSSStationType): Type of the station to filter by.

        Returns:
            List[Station]: List of stations matching the search string and type.
        """
        stations = self.get_stations_by_name(station_name)
        station_type = station_type.value
        
        return [station for station in stations if station.type == station_type]

    def get_stations_by_name(self, name: str, **kwargs) -> List[Stop]:
        """
        Get stations from the VVS API by searching for the name.

        Raises:
            Exception: If the API request fails.
            e: If the JSON response is invalid.

        Returns:
            List[Stop]: List of Stop objects.
        """

        params = {
            "coordOutputFormat": kwargs.get("coordOutputFormat", "WGS84[DD.ddddd]"),
            "name_sf": name,
            "outputFormat": "rapidJSON",
            "type_sf": kwargs.get("type_sf", "any"),
        }

        response_json = self.get("XML_STOPFINDER_REQUEST", params=params)

        self.logger.debug("Initializing parsing of response...")
        return self._parse_response(response_json)

    def _parse_response(self, result: dict) -> List[Stop]:
        parsed_response = []
        if not result or "locations" not in result:
            return []

        if isinstance(result["locations"], dict):
            parsed_response.append(Stop(**result["locations"]))
        elif isinstance(result["locations"], list):
            for station in result["locations"]:
                parsed_response.append(Stop(**station))

        return parsed_response
    

    def calc_trip_time(self, start_station: Station, end_station: Station) -> List[Trip]:
        trips = get_trips(start_station, end_station)
        if trips is None:
            trips = get_trips(end_station, start_station)
        return trips if trips is not None else -1  # Return -1 if no trips are found
    
    def calc_trip(self, start_station: Station, end_station: Station, departure_time: datetime = None, arrival_time: datetime = None) -> Trip:
        """
        Calculate the trip time between two stations.
        """
            
        def get_trip_wrapper(start_station: Station, end_station: Station, departure_time: datetime = None, arrival_time: datetime = None) -> Trip:
            if departure_time is not None and arrival_time is None:
                return get_trips(start_station, end_station, check_time=departure_time, itdDateTimeDepArr="dep", itdTripDateTimeDepArr="dep")
            elif arrival_time is not None and departure_time is None:
                return get_trips(start_station, end_station, check_time=arrival_time, itdDateTimeDepArr="arr", itdTripDateTimeDepArr="arr")
            else:
                raise ValueError("Either departure_time or arrival_time must be set.")
        
        trip_time = get_trip_wrapper(start_station, end_station, departure_time=departure_time, arrival_time=arrival_time)
        if trip_time is None:
            trip_time = get_trip_wrapper(end_station, start_station, departure_time=departure_time, arrival_time=arrival_time)
        if trip_time is None:
            raise ValueError("No trip time found.")
            
        for trip in trip_time:
            # Increment each time by 2h
            for connection in trip.connections:
                connection.origin.departure_time_estimated += datetime.timedelta(hours=2)
                connection.origin.departure_time_planned += datetime.timedelta(hours=2)
                connection.destination.arrival_time_estimated += datetime.timedelta(hours=2)
                connection.destination.arrival_time_planned += datetime.timedelta(hours=2)
            
        return trip_time