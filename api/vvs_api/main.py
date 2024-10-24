import requests  # Add requests import
from typing import List
from vvspy.enums import Station
from vvspy import get_trip
from vvspy.models import Trip
import logging
import datetime
from api.api_client import APIClient

from .stop import Stop, VSSStationType
class VVSAPI(APIClient):
    """
    API client for accessing public transportation data.
    """

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
    
    def search_station(self, station_name: str, type: VSSStationType) -> List[Station]:
        """
        Search for stations by name and filter by station type.

        Args:
            station_name (str): Search string to get mathing stations.
            type (VSSStationType): Type of the station to filter by.

        Returns:
            List[Station]: List of stations matching the search string and type.
        """
        stations = self.get_stations_by_name(station_name)
        type = type.value
        
        return [station for station in stations if station.type == type]

    def get_stations_by_name(self, name: str, request_params: dict = None, session: requests.Session = None, **kwargs) -> List[Stop]:
        """
        Get stations from the VVS API by searching for the name.

        Raises:
            Exception: If the API request fails.
            e: If the JSON response is invalid.

        Returns:
            List[Stop]: List of Stop objects.
        """
        if request_params is None:
            request_params = dict()

        params = {
            "coordOutputFormat": kwargs.get("coordOutputFormat", "WGS84[DD.ddddd]"),
            "name_sf": name,
            "outputFormat": "rapidJSON",
            "type_sf": kwargs.get("type_sf", "any"),
        }

        response_json = self.get("XML_STOPFINDER_REQUEST", params=params)

        self.logger.debug("Initializing parsing of response...")
        try:
            return self._parse_response(response_json)
        except requests.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON.")
            raise e

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
    

    def calc_trip_time(self, start_station: Station, end_station: Station) -> Trip:
        trip_time = get_trip(start_station, end_station)
        if trip_time is None:
            trip_time = get_trip(end_station, start_station)
        return trip_time if trip_time is not None else -1  # Return -1 if no trip time is found
    
    def calc_trip(self, start_station: Station, end_station: Station, start_time: datetime = None) -> Trip:
        trip_time = get_trip(start_station, end_station, check_time=start_time)
        if trip_time is None:
            trip_time = get_trip(end_station, start_station, check_time=start_time)
        return trip_time if trip_time is not None else -1  # Return -1 if no trip time is found
    