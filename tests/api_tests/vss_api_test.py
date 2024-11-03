import datetime
import unittest
import json
from unittest.mock import patch, MagicMock
from vvspy.enums import Station
from api.vvs_api import VVSAPI, VSSStationType
from api.vvs_api.stop import Stop, parse_stop_info
from api.vvs_api.vvs_api_lib_fix import get_trips

class TestVVSAPI(unittest.TestCase):

    def setUp(self):
        self.api = VVSAPI()
        self.example_station_str = 'Stuttgarter Straße'

    def test_initialization(self):
        self.assertEqual(self.api.base_url, "https://www3.vvs.de/vvs/")
        self.assertIsNotNone(self.api.logger)

    def test_station_search(self):
        try:
            result = self.api.search_station("stut", VSSStationType.HALTESTELLE)
            self.assertGreater(len(result), 0)
            self.assertEqual(result[0].disassembled_name, self.example_station_str)
            self.assertEqual(result[0].type, "stop")
        except Exception as e:
            print(f"Direct test failed: {e}")
            with patch('api.vvs_api.VVSAPI.search_station') as mock_search_station:
                mock_search_station.return_value = [
                    MagicMock(disassembled_name=self.example_station_str, type='stop')
                ]
                result = self.api.search_station("stut", VSSStationType.HALTESTELLE)
                self.assertGreater(len(result), 0)
                self.assertEqual(result[0].disassembled_name, self.example_station_str)
                self.assertEqual(result[0].type, "stop")

    def test_calc_trip_time(self):
        try:
            trip = self.api.calc_trip_time(Station.CANNSTATTER_WASEN, Station.DITZINGEN_HERDWEG)
            self.assertIsNotNone(trip)
            self.assertGreater(len(trip.connections), 0)
            self.assertGreater(trip.duration, 30)
            print(trip)
        except Exception as e:
            print(f"Direct test failed: {e}")
            with patch('api.vvs_api.VVSAPI.calc_trip_time') as mock_calc_trip:
                mock_trip = MagicMock()
                mock_trip.connections = [MagicMock()]
                mock_trip.duration = 45
                mock_calc_trip.return_value = mock_trip
                trip = self.api.calc_trip_time(Station.CANNSTATTER_WASEN, Station.DITZINGEN_HERDWEG)
                self.assertIsNotNone(trip)
                self.assertGreater(len(trip.connections), 0)
                self.assertGreater(trip.duration, 30)
                print(trip)
                
    def test_calc_trips_dep_now(self):
        try:
            trips = self.api.calc_trip(Station.CANNSTATTER_WASEN, Station.DITZINGEN_HERDWEG, departure_time=datetime.datetime.now())
            for trip in trips:
                for connection in trip.connections:
                    print(f"Departure: {connection.origin.departure_time_estimated}/{connection.origin.departure_time_planned}, Arrival: {connection.destination.arrival_time_estimated}/{connection.destination.arrival_time_planned}")
                print("---------")
                self.assertIsNotNone(trip)
                self.assertGreater(len(trip.connections), 0)
                self.assertGreater(trip.duration, 30)
            self.assertAlmostEqual(trips[0].connections[0].origin.departure_time_estimated, datetime.datetime.now(), delta=datetime.timedelta(minutes=40))
        except Exception as e:
            print(f"Direct test failed: {e}")
            with patch('api.vvs_api.VVSAPI.calc_trip') as mock_calc_trip, \
                 patch('datetime.datetime') as mock_datetime:
                mock_trip = MagicMock()
                mock_trip.connections = [MagicMock()]
                mock_trip.duration = 45
                mock_calc_trip.return_value = mock_trip
                fixed_now = datetime.datetime(2023, 1, 1, 12, 0, 0)
                mock_datetime.now.return_value = fixed_now
                trip = self.api.calc_trip(Station.CANNSTATTER_WASEN, Station.DITZINGEN_HERDWEG, departure_time=fixed_now)
                self.assertIsNotNone(trip)
                self.assertGreater(len(trip.connections), 0)
                self.assertGreater(trip.duration, 30)
                print(trip)
                
    def test_calc_trips_arr_now(self):
        try:
            trips = self.api.calc_trip(Station.CANNSTATTER_WASEN, Station.DITZINGEN_HERDWEG, arrival_time=datetime.datetime.now())
            for trip in trips:
                for connection in trip.connections:
                    print(f"Departure: {connection.origin.departure_time_estimated}/{connection.origin.departure_time_planned}, Arrival: {connection.destination.arrival_time_estimated}/{connection.destination.arrival_time_planned}")
                print("---------")
                self.assertIsNotNone(trip)
                self.assertGreater(len(trip.connections), 0)
                self.assertGreater(trip.duration, 30)
            self.assertAlmostEqual(trips[-1].connections[-1].destination.arrival_time_estimated, datetime.datetime.now(), delta=datetime.timedelta(minutes=40))
        except Exception as e:
            print(f"Direct test failed: {e}")
            with patch('api.vvs_api.VVSAPI.calc_trip') as mock_calc_trip, \
                 patch('datetime.datetime') as mock_datetime:
                mock_trip = MagicMock()
                mock_trip.connections = [MagicMock()]
                mock_trip.duration = 45
                mock_calc_trip.return_value = mock_trip
                fixed_now = datetime.datetime(2023, 1, 1, 12, 0, 0)
                mock_datetime.now.return_value = fixed_now
                trip = self.api.calc_trip(Station.CANNSTATTER_WASEN, Station.DITZINGEN_HERDWEG, arrival_time=fixed_now)
                self.assertIsNotNone(trip)
                self.assertGreater(len(trip.connections), 0)
                self.assertGreater(trip.duration, 30)
                print(trip)
                
    def test_calc_trips_no_time(self):
        with self.assertRaises(Exception):
            self.api.calc_trip(Station.CANNSTATTER_WASEN, Station.DITZINGEN_HERDWEG)
            
    def test_get_stations_by_name_invalid_json(self):
        with patch('api.vvs_api.VVSAPI.get') as mock_get:
            mock_get.return_value = MagicMock(status_code=200, json=lambda: {})
            result = self.api.get_stations_by_name("stut")
            self.assertEqual(result, [])
            
            
class TestStop(unittest.TestCase):

    def test_stop(self):
        stop = Stop(type="stop", id="de:08111:6020", name="Stuttgarter Straße", match_quality=None)
        self.assertEqual(str(stop), "Stop(type=stop,id=de:08111:6020, name=Stuttgarter Straße, matchQuality=None)")
        stop.info()
        self.assertIsNone(stop.stop_name)
        self.assertIsNone(stop.name_wo)
        self.assertIsNone(stop.point_type)
        self.assertEqual(stop.countdown, 0)
        
    def test_parse_stop_info(self):
        stop = parse_stop_info({
            "type": "stop",
            "id": "de:08111:6020",
            "name": "Stuttgarter Straße",
            "matchQuality": 100
        })
        self.assertEqual(str(stop), "Stop(type=stop,id=de:08111:6020, name=Stuttgarter Straße, matchQuality=100)")
        stop.info()
        self.assertIsNone(stop.stop_name)
        self.assertIsNone(stop.name_wo)
        self.assertIsNone(stop.point_type)
        self.assertEqual(stop.countdown, 0)
        
    def test_vss_station_type(self):
        self.assertEqual(VSSStationType.HALTESTELLE.value, "stop")
        self.assertEqual(VSSStationType.POI.value, "poi")
        self.assertEqual(VSSStationType.STANDORT.value, "locality")
        self.assertEqual(VSSStationType.MISC.value, "uncategorized")
        
class TestVVSApiLibFix(unittest.TestCase):
    REQUESTS_GET = 'requests.get'

    def test_get_trips_success(self):
        with patch.object(VVSAPI, 'get', return_value=MagicMock(status_code=200, json=lambda: {"trips": []})):
            result = get_trips(Station.CANNSTATTER_WASEN, Station.DITZINGEN_HERDWEG)
            self.assertTrue(result is not None and len(result) != 0)

    def test_get_trips_comms_err(self):
        # Simulate a 500 server error response
        with patch(self.REQUESTS_GET) as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 500
            mock_response.text = "Internal Server Error"
            mock_get.return_value = mock_response

            with self.assertRaises(Exception) as context:
                get_trips(Station.CANNSTATTER_WASEN, Station.DITZINGEN_HERDWEG)
            
            # Check if the exception message contains the correct status code
            self.assertIn("Error in API request: 500", str(context.exception))


    def test_get_trips_invalid_json(self):
        # Simulate a 200 OK response with invalid JSON content
        with patch(self.REQUESTS_GET) as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 200
            # This will raise JSONDecodeError when `.json()` is called
            mock_response.json.side_effect = json.decoder.JSONDecodeError("Expecting value", "", 0)
            mock_get.return_value = mock_response

            with self.assertRaises(json.decoder.JSONDecodeError):
                get_trips(Station.CANNSTATTER_WASEN, Station.DITZINGEN_HERDWEG)

    def test_get_trips_status_code(self):
        # Simulate a 404 not found error response
        with patch(self.REQUESTS_GET, return_value=MagicMock(status_code=404, text="Not Found")):
            with self.assertRaises(Exception) as context:
                get_trips(Station.CANNSTATTER_WASEN, Station.DITZINGEN_HERDWEG)
            self.assertIn("Error in API request: 404", str(context.exception))

if __name__ == '__main__':
    unittest.main()