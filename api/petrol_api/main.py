from typing import Dict

import petrol


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
        self.stations = petrol.get_petrol_stations(self.city, self.fuel_name, self.range_km)

    def get_lowest_price_station(self):
        """
        Get the lowest price petrol station.
        """
        if not self.stations:
            self.update_stations()
        return self.stations[0]



if __name__ == "__main__":
    # Example call
    pet1 = PetrolAPI("Stuttgart", "super-e10", 5)
    print(pet1.get_lowest_price_station())