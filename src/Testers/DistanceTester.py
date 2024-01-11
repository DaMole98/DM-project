import unittest

from src.Class_Structures.ClassesDefinition import Trip
from src.Solver_Programs.DistanceMetrics import route_distance, MAX_MINIMAL_DISTANCE, trip_distance


class TestDistance(unittest.TestCase):
    def test_RouteDistance(self):
        print("RouteDistance Test\n")
        # Test Case 1: Empty routes should return MAX_MINIMAL_DISTANCE
        route1 = []
        route2 = []
        print("test1")
        print(f"{route1} {route2}\n\n")
        self.assertEqual(0, route_distance(route1, route2))

        # Test Case 2: Same trip in both routes should return 0
        trip1 = Trip("CityA", "CityB", {"item1": 1, "item2": 2})
        route1 = [trip1]
        route2 = [trip1]
        print("test2")
        print(f"{route1} {route2}\n\n")
        self.assertEqual(0, route_distance(route1, route2))

        # Test Case 3: Different trips with no common items should return MAX_MINIMAL_DISTANCE
        trip1 = Trip("CityA", "CityB", {"item1": 1})
        trip2 = Trip("CityX", "CityY", {"item2": 2})
        route1 = [trip1]
        route2 = [trip2]
        print("test3")
        print(f"{route1} {route2}\n\n")
        self.assertEqual(MAX_MINIMAL_DISTANCE, route_distance(route1, route2))

        # Add more test cases as needed...

    def test_TripDistance(self):
        print("TripDistance Test\n")
        # Test Case 1: Empty routes should return MAX_MINIMAL_DISTANCE
        trip1 = Trip("CityA", "CityB", {"item1": 1, "item2": 2})
        print("test1")
        print(f"{trip1} {None}\n\n")
        self.assertEqual(MAX_MINIMAL_DISTANCE, trip_distance(trip1, None))

        # Test Case 2: Same trip in both routes should return 0
        trip1 = Trip("CityA", "CityB", {"item1": 1, "item2": 2})
        trip2 = Trip("CityA", "CityB", {"item1": 1, "item2": 2})
        print("test2")
        print(f"{trip1} {trip2}\n\n")
        self.assertEqual(0, trip_distance(trip1, trip2))

        # Test Case 3: Different trips with no common items should return MAX_MINIMAL_DISTANCE
        trip1 = Trip("CityA", "CityB", {"item1": 1})
        trip2 = Trip("CityX", "CityY", {"item2": 2})
        print("test3")
        print(f"{trip1} {trip2}\n\n")
        self.assertEqual(MAX_MINIMAL_DISTANCE, trip_distance(trip1, trip2))

        # Add more test cases as needed...

if __name__ == '__main__':
    unittest.main()
