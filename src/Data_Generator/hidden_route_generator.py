from random import random, randint, sample, seed
from src.Class_Structures.ClassesDefinition import HiddenRoute, Trip, Driver


#import the class Trip

#define the class Route
def generate_preferences(drivers, cities, items):
    driver_objects = []

    for driver in drivers:
        city_pref = random.sample(cities, len(cities)) # random permutations of the set
        item_pref = random.sample(items, len(items))
        json_obj = {"driver": driver, "city_pref": city_pref, "item_pref": item_pref}
        driver_objects.append(json_obj)
    return driver_objects



def generate_hidden_routes(drivers, cities, items, limit_trips, limit_items, limit_card):
    """
    **Generate hidden routes for the drivers.**

    :param drivers: List of driver objects for whom hidden routes will be generated.
    :param cities: List of cities that can be included in the hidden routes.
    :param items: List of items that can be associated with trips.
    :param limit_trips: Tuple representing the range (min, max) of trips a driver can undertake.
    :param limit_items: Tuple representing the range (min, max) of items per trip.
    :param limit_card: Tuple representing the range (min, max) of cardinality for each item.

    :return: List of HiddenRoute objects, where each object represents a driver's hidden route.
    :rtype: list

    :algorithm:
    1. For each driver:\n
       - Generate a random number of trips within the specified limit.\n
       - Generate a random permutation of cities to define the route.\n

    2. For each trip:\n
       - Generate a random number of items within the specified limit.\n

    3. For each item:\n
       - Generate a random item from the provided list.\n
       - Generate a random cardinality within the specified limit.\n

    4. Build the hidden route structure:\n
       - Create a HiddenRoute object for the driver.\n
       - Create a Trip object for each trip, associating generated items and cities.\n
       - Append the trip to the driver's hidden route.\n

    5. Return the list of generated hidden routes.
    """
    hidden_routes = []
    for driver in drivers:
        trip_number = randint(limit_trips[0], limit_trips[1])
        route_cities = sample(cities, trip_number + 1)
        hd_route = HiddenRoute(id = f'h{driver.id}', driver_id = driver.id, length = trip_number, route = [])

        for i in range(0, trip_number):
            trip_items = []
            item_number = randint(limit_items[0], limit_items[1])
            item_types = sample(items, randint(limit_items[0], limit_items[1]))
            merch = {item: randint(limit_card[0], limit_card[1]) for item in
                     item_types}  # generation of the merchandise of a trip
            hd_route.route.append(Trip(route_cities[i], route_cities[i + 1], merch))
        hidden_routes.append(hd_route)

        driver.hidden_route = hd_route

    return hidden_routes

