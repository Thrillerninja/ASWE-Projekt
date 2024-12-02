weather_conditions = {
    # Thunderstorm (Gruppe 2xx)
    200: {"description": "es wird ein Gewitter mit leichtem Regen erwartet.", "icon": "11d"},
    201: {"description": "es wird ein Gewitter mit Regen erwartet.", "icon": "11d"},
    202: {"description": "es wird ein Gewitter mit starkem Regen erwartet.", "icon": "11d"},
    210: {"description": "es wird ein leichtes Gewitter geben.", "icon": "11d"},
    211: {"description": "es wird ein Gewitter geben.", "icon": "11d"},
    212: {"description": "es wird ein starkes Gewitter geben.", "icon": "11d"},
    221: {"description": "es wird ein unregelmäßiges Gewitter geben.", "icon": "11d"},
    230: {"description": "es wird ein Gewitter mit leichtem Nieselregen geben.", "icon": "11d"},
    231: {"description": "es wird ein Gewitter mit Nieselregen geben.", "icon": "11d"},
    232: {"description": "es wird ein Gewitter mit starkem Nieselregen geben.", "icon": "11d"},
    
    # Drizzle (Gruppe 3xx)
    300: {"description": "es wird leichter Nieselregen erwartet.", "icon": "09d"},
    301: {"description": "es wird Nieselregen erwartet.", "icon": "09d"},
    302: {"description": "es wird starker Nieselregen erwartet.", "icon": "09d"},
    310: {"description": "es wird leichter Nieselregen mit Regen erwartet.", "icon": "09d"},
    311: {"description": "es wird Nieselregen mit Regen erwartet.", "icon": "09d"},
    312: {"description": "es wird starker Nieselregen mit Regen erwartet.", "icon": "09d"},
    313: {"description": "es wird Regenschauer mit Nieselregen geben.", "icon": "09d"},
    314: {"description": "es wird starker Regenschauer mit Nieselregen geben.", "icon": "09d"},
    321: {"description": "es wird Schauernieselregen geben.", "icon": "09d"},
    
    # Rain (Gruppe 5xx)
    500: {"description": "es wird leichter Regen erwartet.", "icon": "10d"},
    501: {"description": "es wird mäßiger Regen erwartet.", "icon": "10d"},
    502: {"description": "es wird starker Regen erwartet.", "icon": "10d"},
    503: {"description": "es wird sehr starker Regen erwartet.", "icon": "10d"},
    504: {"description": "es wird extremer Regen erwartet.", "icon": "10d"},
    511: {"description": "es wird gefrierender Regen erwartet.", "icon": "13d"},
    520: {"description": "es wird leichter Regenschauer erwartet.", "icon": "09d"},
    521: {"description": "es wird Regenschauer erwartet.", "icon": "09d"},
    522: {"description": "es wird starker Regenschauer erwartet.", "icon": "09d"},
    531: {"description": "es wird ein unregelmäßiger Regenschauer erwartet.", "icon": "09d"},
    
    # Snow (Gruppe 6xx)
    600: {"description": "es wird leichter Schneefall erwartet.", "icon": "13d"},
    601: {"description": "es wird Schneefall erwartet.", "icon": "13d"},
    602: {"description": "es wird starker Schneefall erwartet.", "icon": "13d"},
    611: {"description": "es wird Schneeregen erwartet.", "icon": "13d"},
    612: {"description": "es wird leichter Schneeregen erwartet.", "icon": "13d"},
    613: {"description": "es wird Schneeregenschauer geben.", "icon": "13d"},
    615: {"description": "es wird leichter Regen mit Schnee erwartet.", "icon": "13d"},
    616: {"description": "es wird Regen mit Schnee erwartet.", "icon": "13d"},
    620: {"description": "es wird leichter Schneeschauer erwartet.", "icon": "13d"},
    621: {"description": "es wird Schneeschauer erwartet.", "icon": "13d"},
    622: {"description": "es wird starker Schneeschauer erwartet.", "icon": "13d"},
    
    # Atmosphere (Gruppe 7xx)
    701: {"description": "es wird neblig sein.", "icon": "50d"},
    711: {"description": "es wird Rauch in der Luft geben.", "icon": "50d"},
    721: {"description": "es wird dunstig sein.", "icon": "50d"},
    731: {"description": "es werden Sand- oder Staubwirbel auftreten.", "icon": "50d"},
    741: {"description": "es wird neblig sein.", "icon": "50d"},
    751: {"description": "es wird sandig sein.", "icon": "50d"},
    761: {"description": "es wird staubig sein.", "icon": "50d"},
    762: {"description": "es wird Vulkanasche in der Luft geben.", "icon": "50d"},
    771: {"description": "es wird böig sein.", "icon": "50d"},
    781: {"description": "es wird einen Tornado geben.", "icon": "50d"},
    
    # Clear (Gruppe 800)
    800: {"description": "der Himmel wird klar sein.", "icon": "01d"},
    
    # Clouds (Gruppe 80x)
    801: {"description": "es wird nur wenige Wolken geben.", "icon": "02d"},
    802: {"description": "es werden vereinzelte Wolken am Himmel sein.", "icon": "03d"},
    803: {"description": "es wird bewölkt sein.", "icon": "04d"},
    804: {"description": "es wird stark bewölkt sein.", "icon": "04d"}
}

__all__ = ['weather_conditions']