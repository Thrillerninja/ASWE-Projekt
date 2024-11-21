import unittest
from bs4 import BeautifulSoup

from api.petrol_api.main import PetrolAPI
from api.petrol_api.petrol import GasStation, get_soup, get_average_price, get_gas_stations


class TestPetrol(unittest.TestCase):

    # Testen der Station-Klasse
    def test_station_class(self):
        station = GasStation("Shell", 1.50)
        self.assertEqual(str(station), repr(station))
        self.assertEqual(station.name, "Shell")
        self.assertEqual(station.price, 1.50)

    # Testen der get_soup Funktion
    def test_get_soup(self):
        soup = get_soup("Stuttgart", "super-e10", 5)
        self.assertIsInstance(soup, BeautifulSoup)
        self.assertIsNotNone(soup.find("div", class_="city-price-average"))

    # Testen der get_average_price Funktion
    def test_get_average_price(self):
        city, fuel, price = get_average_price("Stuttgart", "super-e10", 5)
        self.assertIsInstance(city, str)
        self.assertIsInstance(fuel, str)
        self.assertIsInstance(price, float)

    # Testen der get_gas_stations Funktion
    def test_get_gas_stations(self):
        stations = get_gas_stations("Stuttgart", "super-e10", 5)
        self.assertNotEqual(len(stations), 0)
        station = stations[0]
        self.assertIsInstance(station, GasStation)
        self.assertIsInstance(station.price, float)
        self.assertIsInstance(station.name, str)

    # Testen von ungültigem Kraftstoff
    def test_invalid_fuel(self):
        with self.assertRaises(AssertionError) as excinfo:
            get_soup("Stuttgart", "invalid-fuel", 5)
        self.assertIn("Fuel type invalid-fuel not found", str(excinfo.exception))


class TestPetrolAPI(unittest.TestCase):
    # Testen der PetrolAPI-Klasse
    def test_petrol_api(self):
        api = PetrolAPI(city="Stuttgart", fuel_name="super-e10", range_km=5)
        api.update_stations()
        self.assertIsInstance(api.stations, list)
        self.assertNotEqual(len(api.stations), 0)
        lowest = api.get_current_lowest_price()
        self.assertIsInstance(lowest, float)


if __name__ == '__main__':
    unittest.main()