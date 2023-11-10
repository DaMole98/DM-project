import dataclasses
from dataclasses import dataclass
import json
import random

@dataclass
class Trip:
    departure: str
    destination: str
    merchandise: dict[str, int] #JUST FOR TYPE HINTING!! PYTHON IS DINAMICALLY TYPED. DONT MESS WITH TYPES PLS :)

@dataclass
class StandardRoute:
    id: str
    route: list[Trip]

@dataclass
class ActualRoute:
    id: str
    driver: str
    sroute: str
    route: list[Trip]


# overriding of the standard encoder in order to make it accept dataclasses
class EnhancedJSONEncoder(json.JSONEncoder):
        def default(self, o):
            if dataclasses.is_dataclass(o):
                return dataclasses.asdict(o)
            return super().default(o)
        

'''
generates driver preferences
@params drivers is a json-like object that contains the drivers (this case a list)
Same for cities and items.
returns a a python object that can be json-formatted as following:

[
    {
        "driver" : "A"
        "city_pref" : ["Venezia", "Bergamo", "Trieste"]
        "item_pref" : ["tomatoes", "potatoes", "otheratoes"]
    }
    {
        "driver": "B"
        .
        .
        .
    }

]
'''

def generate_preferences(drivers, cities, items):
    driver_objects = []

    for driver in drivers:
        city_pref = random.sample(cities, len(cities)) # random permutations of the set
        item_pref = random.sample(items, len(items))
        json_obj = {"driver": driver, "city_pref": city_pref, "item_pref": item_pref}
        driver_objects.append(json_obj)
    return driver_objects






if __name__ == "__main__":

    import os

    entropy = os.urandom(128) # set entropy to a number as desired to make the results reproducible
    random.seed(entropy)


    data_path = "./data/"
    dev_data_path = f"{data_path}/dev_data/"

    with open(f"{dev_data_path}cities.json", 'r') as file:
        cities = json.load(file)

    with open(f"{dev_data_path}items.json", 'r') as file:
        items = json.load(file)

    '''
    create random standard routes (generate standard.json)
    '''

    std_routes_num = 10 #number of routes to be generated
    min_trips = 1
    max_trips = 5 #bounds on the number of trips per route. Ensure that this value does not exceed hte number of cities minus one
                   #(otherwise the same city will appear more times in a route. This could make sense in certain cases)
    min_items = 1
    max_items = 10 #maximum number of types of items per trip

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


    # Serialize to JSON with the enhanced encoder
    json_data = json.loads(json.dumps(route_list, cls=EnhancedJSONEncoder))

    # renaming the keys (cant do it in dataclass definition because the 'from' word clashes with the python keyword)
    for route in json_data:
        for trip in route['route']:
            trip['from'] = trip.pop('departure')
            trip['to'] = trip.pop('destination')
            trip['merchandise'] = trip.pop('merchandise')


    # Dump the modified data to a JSON file with indentation
    with open(f"{data_path}standard.json", "w") as file:
        json.dump(json_data, file, indent=2)


    ###########################################################################    

    '''
    Generate the actual.json from the standard.json generated above
    '''
    #load drivers
    with open(f"{dev_data_path}drivers.json", 'r') as file:
        drivers = json.load(file)
    
    act_routes_num = 100

    '''
    every route implementation has a (high) probability of being mutated with respect to the original standard route.
    Although almost every time the drives introduce mutations to the plan, this is not always happening.
    To model this, we create an array of samples from a bernoulli with parameter p of length act_routes_num, in which 1
    means that the actual route is mutated with respect to the standard route and 0 means that the driver sticked to the plan

    Now, that said, the driver does not just introduce random noise (or, at least, this is not happening in the reality) since the driver changes the plan
    following his own ppersonal preferences. Thus, we need a way to simulate the personal preferences. We do this by creating permutations of the parameter
    sets (that are cities, item types) for each driver: these permutations indicate the driver preferences (e.g. if driver A has Venice as the first element of
    the permutation of the cities set, this means that Venice is his favourite city, and then if Bergamo is the second in the permutation, this means that Bergamo
    is the second preference of the driver A, and so on...).
    For the set of items it is worth to note that the driver preference affects 2 parameters of the
    standard routes: the set of items carried and the number of items of a specific types. For example, if driver A likes tomatoes means that it is possible that
    in his trips it will take with him tomatoes even if it is not planned in the standard route, or if the standard route involves bringing tomatoes the driver could
    add some extra tomatoes because he likes to eat tomatoes during the journey. 
    '''
    drivers_preferences = generate_preferences(drivers, cities, items)

    with open(f"{dev_data_path}drivers_prefs.json", "w") as file:
        json.dump(drivers_preferences, file, indent=2)


#    p = 0.9
#    mut_bitmap = [1 if random.random() < p else 0 for _ in range(act_routes_num)]

#    for rt, sample in enumerate(mut_bitmap):
#        #have to pick one standard route and add noise into its implementation, i.e. driver could change the endpoints of a trip
#        #(by adding a city, so adding a trip, or by omitting a trip, thus skipping a city), change the quantity of items and even the item types (by omitting some of them or adding some random item types).
#        if sample != 0:
#            std_route = json_data[i] #standard route from which this route is implemented


#            ActualRoute(f"a{rt}", driver, sroute, route)

#        else: continue
    

