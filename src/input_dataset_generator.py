import dataclasses
from dataclasses import dataclass
import json


@dataclass
class Trip:
    departure: str
    destination: str
    merchandise: dict[str, int] #JUST FOR TYPE HINTING!! PYTHON IS DINAMICALLY TYPED. DONT MESS WITH TYPES PLS :)

@dataclass
class StandardRoute:
    id: str
    route: list[Trip]


# overriding of the standard encoder in order to make it accept dataclasses
class EnhancedJSONEncoder(json.JSONEncoder):
        def default(self, o):
            if dataclasses.is_dataclass(o):
                return dataclasses.asdict(o)
            return super().default(o)



if __name__ == "__main__":

    import os
    import random

    entropy = os.urandom(128)
    random.seed(entropy)


    data_path = "./data/"

    with open(f"{data_path}cities.json", 'r') as file:
        cities = json.load(file)

    with open(f"{data_path}items.json", 'r') as file:
        items = json.load(file)

    '''
    create random standard routes
    '''

    std_routes_num = 10 #number of routes to be generated
    min_trips = 1
    max_trips = 10 #bounds on the number of trips per route. Ensure that this value does not exceed hte number of cities minus one
                   #(otherwise the same city will appear more times in a route. This could make sense in certain cases)
    min_items = 1
    max_items = 5 #maximum number of types of items per trip

    min_card=1
    max_card=50 #cardinality of a specified item in a trip

    route_list =[]
    for rt in range(std_routes_num):
        trip_number = random.randint(min_trips, max_trips)
        route_cities = random.sample(cities, trip_number + 1) # cities on the route

        trip_list = []
        for trp in range(trip_number):
            item_types = random.sample(items, random.randint(min_items, max_items))
            merch = {item : random.randint(min_card, max_card) for item in item_types} #generation of the merchandise of a trip
            trip_list.append(Trip(route_cities[trp], route_cities[trp+1], merch))

        
        route_list.append(StandardRoute(f"s{rt}", trip_list))


    # Serialize to JSON with the original encoder
    json_data = json.loads(json.dumps(route_list, cls=EnhancedJSONEncoder))

    for route in json_data:
        for trip in route['route']:
            trip['from'] = trip.pop('departure')
            trip['to'] = trip.pop('destination')


    # Dump the modified data to a JSON file with indentation
    with open(f"{data_path}standard.json", "w") as file:
        json.dump(json_data, file, indent=2)



