weather_conditions = {
    # Thunderstorm (Gruppe 2xx)
    200: {"description": "Gewitter mit leichtem Regen", "icon": "11d"},
    201: {"description": "Gewitter mit Regen", "icon": "11d"},
    202: {"description": "Gewitter mit starkem Regen", "icon": "11d"},
    210: {"description": "Leichtes Gewitter", "icon": "11d"},
    211: {"description": "Gewitter", "icon": "11d"},
    212: {"description": "Starkes Gewitter", "icon": "11d"},
    221: {"description": "Unregelmäßiges Gewitter", "icon": "11d"},
    230: {"description": "Gewitter mit leichtem Nieselregen", "icon": "11d"},
    231: {"description": "Gewitter mit Nieselregen", "icon": "11d"},
    232: {"description": "Gewitter mit starkem Nieselregen", "icon": "11d"},
    
    # Drizzle (Gruppe 3xx)
    300: {"description": "Leichter Nieselregen", "icon": "09d"},
    301: {"description": "Nieselregen", "icon": "09d"},
    302: {"description": "Starker Nieselregen", "icon": "09d"},
    310: {"description": "Leichter Nieselregen und Regen", "icon": "09d"},
    311: {"description": "Nieselregen und Regen", "icon": "09d"},
    312: {"description": "Starker Nieselregen und Regen", "icon": "09d"},
    313: {"description": "Regenschauer und Nieselregen", "icon": "09d"},
    314: {"description": "Starker Regenschauer und Nieselregen", "icon": "09d"},
    321: {"description": "Schauernieselregen", "icon": "09d"},
    
    # Rain (Gruppe 5xx)
    500: {"description": "Leichter Regen", "icon": "10d"},
    501: {"description": "Mäßiger Regen", "icon": "10d"},
    502: {"description": "Starker Regen", "icon": "10d"},
    503: {"description": "Sehr starker Regen", "icon": "10d"},
    504: {"description": "Extremer Regen", "icon": "10d"},
    511: {"description": "Gefrierender Regen", "icon": "13d"},
    520: {"description": "Leichter Regenschauer", "icon": "09d"},
    521: {"description": "Regenschauer", "icon": "09d"},
    522: {"description": "Starker Regenschauer", "icon": "09d"},
    531: {"description": "Unregelmäßiger Regenschauer", "icon": "09d"},
    
    # Snow (Gruppe 6xx)
    600: {"description": "Leichter Schnee", "icon": "13d"},
    601: {"description": "Schnee", "icon": "13d"},
    602: {"description": "Starker Schnee", "icon": "13d"},
    611: {"description": "Schneeregen", "icon": "13d"},
    612: {"description": "Leichter Schneeregen", "icon": "13d"},
    613: {"description": "Schneeregenschauer", "icon": "13d"},
    615: {"description": "Leichter Regen und Schnee", "icon": "13d"},
    616: {"description": "Regen und Schnee", "icon": "13d"},
    620: {"description": "Leichter Schneeschauer", "icon": "13d"},
    621: {"description": "Schneeschauer", "icon": "13d"},
    622: {"description": "Starker Schneeschauer", "icon": "13d"},
    
    # Atmosphere (Gruppe 7xx)
    701: {"description": "Nebel", "icon": "50d"},
    711: {"description": "Rauch", "icon": "50d"},
    721: {"description": "Dunst", "icon": "50d"},
    731: {"description": "Sand-/Staubwirbel", "icon": "50d"},
    741: {"description": "Nebel", "icon": "50d"},
    751: {"description": "Sand", "icon": "50d"},
    761: {"description": "Staub", "icon": "50d"},
    762: {"description": "Vulkanasche", "icon": "50d"},
    771: {"description": "Böen", "icon": "50d"},
    781: {"description": "Tornado", "icon": "50d"},
    
    # Clear (Gruppe 800)
    800: {"description": "Klarer Himmel", "icon": "01d"},
    
    # Clouds (Gruppe 80x)
    801: {"description": "Wenige Wolkeny", "icon": "02d"},
    802: {"description": "Vereinzelte Wolken", "icon": "03d"},
    803: {"description": "Bewölkt", "icon": "04d"},
    804: {"description": "Stark bewölkt", "icon": "04d"}
}

__all__ = ['weather_conditions']