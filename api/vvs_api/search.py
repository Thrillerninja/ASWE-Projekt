import json
from typing import List
import requests
import logging

from stop import Stop

__API_URL = f"https://www3.vvs.de/vvs/XML_STOPFINDER_REQUEST?"
logger = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)

def search_stations_by_name(
    name: str,
    request_params: dict = None,
    return_response: bool = False,
    session: requests.Session = None,
    **kwargs,
) -> List[Stop]:
    """
    Search for stations/stops by their name.

    Parameters:
    name (str): The name of the station/stop to search for.
    request_params (dict, optional): Additional request parameters.
    return_response (bool, optional): Whether to return the response object.
    session (requests.Session, optional): The session to use for requests.
    kwargs: Additional keyword arguments.

    Returns:
    List[Stop]: A list of matching Stop objects.
    """
    
    if request_params is None:
        request_params = dict()
        
    # Construct the parameters for the API request
    params = {
        "coordOutputFormat": kwargs.get("coordOutputFormat", "WGS84[DD.ddddd]"),
        "name_sf": name,
        "outputFormat": "rapidJSON",
        "type_sf": kwargs.get("type_sf", "any"),        
    }
    
    # Make the API request using the provided session or a new one
    if session:
        r = session.get(__API_URL, **{**request_params, **{"params": params}})
    else:
        r = requests.get(__API_URL, **{**request_params, **{"params": params}})
        
    logger.debug(f"Request took {r.elapsed.total_seconds()}s and returned {r.status_code}")
    
    # Check for errors in the API response
    if r.status_code != 200:
        logger.error("Error in API request")
        logger.error(f"Request: {r.status_code}")
        logger.error(f"{r.text}")
        raise Exception(f"Error in API request: {r.status_code}")
    
    if return_response:
        return r
    
    logger.debug("Initializing parsing of response...")
    
    try:
        r.encoding = "UTF-8"
        return _parse_response(r.json())
    except json.decoder.JSONDecodeError as e:
        logger.error("Error in API request. Received invalid JSON. Status code: %s", r.status_code)
        raise e
        
def _parse_response(result: dict) -> List[Stop]:
    """
    Parse the API response to extract station information.

    Parameters:
    result (dict): The JSON response from the API.

    Returns:
    List[Stop]: A list of Train stop objects parsed from the response.
    """
    parsed_response = []
    if (
        not result or "locations" not in result or not result["locations"]
    ):  # error in response/request
        return []  # no results

    if isinstance(result["locations"], dict):  # one result
        parsed_response.append(Stop(**result["locations"]))
    elif isinstance(result["locations"], list):  # multiple results
        for station in result["locations"]:
            parsed_response.append(Stop(**station))

    return parsed_response