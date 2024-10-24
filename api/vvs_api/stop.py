import json
from datetime import datetime
from typing import List, Optional, Dict
from enum import Enum

class Stop:
    def __init__(self, **kwargs):
        r"""
        
        Stop object from a search request.
        
        Attributes
        -----------
        
        id :class:`str`
            ID of the stop.
        is_global_id :class:`bool`
            If the ID is global.
        name :class:`str`
            Name of the stop.
        disassembled_name :class:`str`
            Disassembled name of the stop.
        coord :class:`List[float]`
            Coordinates of the stop.
        type :class:`str`
            Type of the stop.
        match_quality :class:`int`
            Match quality of the stop.
        is_best :class:`bool`
            If the stop is the best match.
        product_classes :class:`List[int]`
            Product classes of the stop. Oberserved Values: 0=Train, 5 or 10 Bus
        parent :class:`dict`
            Parent of the stop.
        assigned_stops :class:`List[dict]`
            Assigned stops of the stop.
        properties :class:`dict`
            Properties of the stop.
        area :class:`str`
            Area of the stop.
        platform :class:`str`
            Platform of the stop.
        platform_name :class:`str`
            Name of the platform.
        stop_name :class:`str`
            Name of the stop.
        name_wo :class:`str`
            Name of the stop.
        point_type :class:`str`
            Type of the point.
        countdown :class:`int`
            Countdown of the stop.
        """
        
        self.id = kwargs.get("id")
        self.is_global_id = kwargs.get("isGlobalId")
        self.name = kwargs.get("name")
        self.disassembled_name = kwargs.get("disassembledName")
        self.coord = kwargs.get("coord", [])
        self.type = kwargs.get("type")
        self.match_quality = kwargs.get("matchQuality")
        self.is_best = kwargs.get("isBest")
        self.product_classes = kwargs.get("productClasses", [])
        self.parent = kwargs.get("parent", {})
        self.assigned_stops = kwargs.get("assignedStops", [])
        self.properties = kwargs.get("properties", {})
        self.area = kwargs.get("area")
        self.platform = kwargs.get("platform")
        self.platform_name = kwargs.get("platformName")
        self.stop_name = kwargs.get("stopName")
        self.name_wo = kwargs.get("nameWO")
        self.point_type = kwargs.get("pointType")
        self.countdown = int(kwargs.get("countdown", "0"))

    def __str__(self):
        return f"Stop(type={self.type},id={self.id}, name={self.name}, matchQuality={self.match_quality})"
    
    def info(self):
        # Print all info
        print(f"ID: {self.id}")
        print(f"Name: {self.name}")
        print(f"Disassembled Name: {self.disassembled_name}")
        print(f"Coordinates: {self.coord}")
        print(f"Type: {self.type}")
        print(f"Match Quality: {self.match_quality}")
        print(f"Is Best: {self.is_best}")
        print(f"Product Classes: {self.product_classes}")
        print(f"Parent: {self.parent}")
        print(f"Assigned Stops: {self.assigned_stops}")
        print(f"Properties: {self.properties}")
        print(f"Area: {self.area}")
        print(f"Platform: {self.platform}")
        print(f"Platform Name: {self.platform_name}")
        print(f"Stop Name: {self.stop_name}")
        print(f"Name WO: {self.name_wo}")
        print(f"Point Type: {self.point_type}")
        print(f"Countdown: {self.countdown}")
        

def parse_stop_info(json_data: Dict) -> Stop:
    """
    Parse the JSON data to create a Stop object.

    Parameters:
    json_data (dict): The JSON data to parse.

    Returns:
    Stop: The parsed Stop object.
    """
    return Stop(**json_data)



class VSSStationType(Enum):
    """
    Enum class for different types of stations.
    """
    HALTESTELLE = "stop"
    POI = "poi"
    STANDORT = "locality"
    MISC = "uncategorized"
    
    
class VVSProdukte(Enum):
    """
    Enum class for different types of transport services.
    """
    X1=0
    X2=1 #TODO: Valid descriptors
    X3=3
    X4=5
    X5=11