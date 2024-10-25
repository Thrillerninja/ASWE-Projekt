import pytest
import re
from bs4 import BeautifulSoup

from petrol import Station, get_soup, get_average_price, get_petrol_stations

# Testen der Station-Klasse
def test_station_class():
    station = Station("Shell", 1.50)
    assert str(station) == repr(station)
    assert station.name == "Shell"
    assert station.price == 1.50


# Testen der get_soup Funktion
def test_get_soup():
    soup = get_soup("Stuttgart", "super-e10", 5)
    assert isinstance(soup, BeautifulSoup)
    assert soup.find("div", class_="city-price-average") is not None


# Testen der get_average_price Funktion
def test_get_average_price():
    city, fuel, price = get_average_price("Stuttgart", "super-e10", 5)
    assert isinstance(city, str)
    assert isinstance(fuel, str)
    assert isinstance(price, float)


# Testen der get_petrol_stations Funktion
def test_get_petrol_stations():
    stations = get_petrol_stations("Stuttgart", "super-e10", 5)
    assert len(stations) != 0
    station = stations[0]
    assert isinstance(station, Station)
    assert isinstance(station.price, float)
    assert isinstance(station.name, str)


# Testen von ungültigem Kraftstoff
def test_invalid_fuel():
    with pytest.raises(AssertionError) as excinfo:
        get_soup("Stuttgart", "invalid-fuel", 5)
    assert "Fuel type invalid-fuel not found" in str(excinfo.value)
