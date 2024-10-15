import requests
from bs4 import BeautifulSoup


class Station:
    def __init__(self, name, price):
        self.name = name
        self.price = price
    
    def __str__(self) -> str:
        return f"{self.name}: {self.price}"
    def __repr__(self) -> str:
        return self.__str__()



def get_petrol_stations(city, fuel_name, range_km):
    '''
    Get gas prices for a city and fuel type
    - param `city`: City name
    - param `fuel_name`: Fuel type
        - super-e10
        - super-e5
        - super-plus
        - diesel
        - lkw-diesel
        - lpg
    - param `range_km`: Range in km
    - return: List of stations (lowest price first)
    '''
    

    city = city.replace(" ", "+")
    fuels  = {
        "lpg": 1,
        "lkw-diesel": 2,
        "diesel": 3,
        "super-e10": 5,
        "super-plus": 6,
        "super-e5": 7
    }
    fuel_type = fuels.get(fuel_name)
    assert fuel_type, f"Fuel type {fuel_name} not found. Choose from {list(fuels.keys())}"

    url = f"https://www.clever-tanken.de/tankstelle_liste?ort={city}&spritsorte={fuel_type}&r={range_km}"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # ========================
    # Get Average price
    # ========================

    # avg_city_average_obj = soup.find("div", class_="city-price-average")
    # avg_fuel = avg_city_average_obj.find("span").text
    # avg_city = avg_city_average_obj.find_all("span")[1].text
    # avg_value = avg_city_average_obj.find("div", class_="city-price-average-text").text
    # print(f"{avg_fuel} in {avg_city} is {avg_value}")
    # TODO: average preis im umkreis wird nicht genutzt. sollte es genutzt werden?
    # Eigentlich interessiert ja nur der günstigste Preis...

    # ========================
    # Collect stations
    # ========================
    
    stations = []
    # Get data from script-element
    script = [script for script in soup.find_all("script") if "addPoi" in script.text][0].text
    lines = [l for l in script.split("\n") if "addPoi" in l and "Standort" not in l]
    # Add stations to list
    for line in lines:
        if len(line.split("\'")) < 10: continue
        name = line.split("\'")[7]
        price = line.split("\'")[9]
        stations.append(Station(name, price))
    # sort by price (lowest first)
    stations.sort(key=lambda x: x.price)
    return stations



if __name__ == "__main__":
    # Example call
    get_petrol_stations("Stuttgart", "super-e10", 5)
