from typing import Dict

from .petrol import get_gas_stations

class PetrolAPI():
    """
    API client for accessing petrol prices.
    """

    def __init__(self, city:str="Stuttgart", fuel_name:str="super-e10", range_km:int=5):
        self.city = city  # can be a city name or a postal code
        self.fuel_name = fuel_name
        self.range_km = range_km
        self.stations = []
        self.update_stations()  # get the stations


    def update_stations(self):
        """
        Updates the petrol stations.
        """
        self.stations = get_gas_stations(self.city, self.fuel_name, self.range_km)

    def get_lowest_price_station(self):
        """
        Get the lowest price petrol station.
        """
        if not self.stations:
            self.update_stations()
        return self.stations[0]