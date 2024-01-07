import dataclasses
import json
from random import randint, seed, sample, shuffle

from src.Class_Structures.ClassesDefinition import *
from src.Data_Generator.Parameters.parameters import *
from src.Data_Generator.actual_route_generator import generate_actual_route
from src.Data_Generator.hidden_route_generator import generate_hidden_routes


# overriding of the standard encoder in order to make it accept dataclasses
class EnhancedJSONEncoder(json.JSONEncoder):
        def default(self, o):
            if dataclasses.is_dataclass(o):
                return dataclasses.asdict(o)
            return super().default(o)


DEBUG = True

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

if __name__ == "__main__":

    import os

    entropy = os.urandom(128) # set entropy to a number as desired to make the results reproducible
    seed(entropy)

    # start timer
    import time
    start = time.time()

    with open(f"{dev_data_path}cities.json", 'r') as file:
        cities = json.load(file)

    with open(f"{dev_data_path}items.json", 'r') as file:
        items = json.load(file)

    '''
    create random standard routes (generate standard.json)
    '''

    size_dataset += "_dataset"

    if DEBUG:
        print(f"Generating {size_dataset}...")

    route_list =[]
    for rt in range(std_routes_num):
        trip_number = randint(min_trips, max_trips)
        route_cities = sample(cities, min(len(cities),trip_number + 1)) # cities on the route

        trip_list = []
        for trp in range(trip_number):
            try:
                item_types = sample(items, randint(min_items, max_items))
            except ValueError:
                print("The number of items is greater than the number of items in the dataset")
                exit(1)
            merch = {item: randint(min_card, max_card) for item in item_types} #generation of the merchandise of a trip
            trip_list.append(Trip(route_cities[(trp%len(route_cities))], route_cities[(trp+1)%len(cities)], merch))
            if trp %len(route_cities) == 0:
                shuffle(route_cities)

        
        route_list.append(StandardRoute(f"s{rt}", trip_list))

    if DEBUG:
        time_flag = time.time()
        print("standard routes generated in time: ", time_flag - start)


    # Serialize to JSON with the enhanced encoder
    json_data = json.loads(json.dumps(route_list, cls=EnhancedJSONEncoder))

    # renaming the keys (cant do it in dataclass definition because the 'from' word clashes with the python keyword)
    for route in json_data:
        for trip in route['route']:
            trip['from'] = trip.pop('departure')
            trip['to'] = trip.pop('destination')
            trip['merchandise'] = trip.pop('merchandise')


    try:
        # Dump the modified data to a JSON file with indentation
        with open(f"{data_path}/{size_dataset}/standard.json", "w") as file:
            json.dump(json_data, file, indent=2)
    except FileNotFoundError:
        print("File not found"+f"{data_path}/{size_dataset}/standard.json")
        exit(1)

    if DEBUG:
        time_flag_tmp = time.time()
        print("standard.json generated in time: ", time_flag_tmp - time_flag)
        time_flag = time_flag_tmp

    '''
    Generate the actual.json from the standard.json generated above
    '''

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
    # drivers_preferences = generate_preferences(drivers, cities, items)
    #
    # with open(f"{dev_data_path}drivers_prefs.json", "w") as file:
    #     json.dump(drivers_preferences, file, indent=2)

    # transform the json data drivers to a list of Driver objects, so id: str, hidden_route: None4
    drivers= []
    for i in range(1, num_drivers):
        # create a new driver object with id = (A + (i%26) ) * (i//26)
        id = chr(ord('A') + (i % 26))
        if i // 26 > 0:
            id = chr(ord(id)) * (i // 26)
        if DEBUG:
            print(f"driver {id} generated")
        new_driver = Driver(id, None)
        drivers.append(new_driver)

    if DEBUG:
        print("drivers generated")
        print(drivers)

    limit_trip = [min_trips, max_trips]
    limit_items = [min_items, max_items]
    limit_card = [min_card, max_card]

    hidden_routes = generate_hidden_routes(drivers, cities, items, limit_trip, limit_items, limit_card)

    if DEBUG:
        time_flag_tmp = time.time()
        print("hidden routes generated in time: ", time_flag_tmp - time_flag)
        time_flag = time.time()

    # Serialize to JSON with the enhanced encoder
    json_data = json.loads(json.dumps(hidden_routes, cls=EnhancedJSONEncoder))

    # create new file with the Driver objects and the hidden routes
    try:
        create_file = open(f"{data_path}/{size_dataset}/HiddenRoutes.json", "x")
        create_file.close()
    except FileExistsError:
        pass

    try:
        with open(f"{data_path}/{size_dataset}/HiddenRoutes.json", "w") as file:
            json.dump(json_data, file, indent=2)
    except FileNotFoundError:
        print("File not found")
        exit(1)

    if DEBUG:
        print("hidden routes dumped in file in time: ", time.time() - time_flag)
        time_flag = time.time()

    ID = 0
    actual_routes = []

    for driver in drivers:
        # take a sample of std_routes_num standard routes
        num_of_routes = randint(1, MAX_STD_ROUTE_PER_DRIVER)
        sroutes = sample(route_list, num_of_routes)

        # for each standard route, generate a random number of implementations
        for sroute in sroutes:
            num_of_implementations = randint(1, MAX_IMPLEMENTATIONS_PER_DRIVER)
            for _ in range(num_of_implementations):
                # generate an actual route from the standard route
                route = generate_actual_route(driver.hidden_route,sroute, cities, items, driver.id)
                new_actual_route = ActualRoute(f"a{ID}", driver.id, sroute.id, route.route)
                actual_routes.append(new_actual_route)
                ID += 1

    if DEBUG:
        print("actual routes generated in time: ", time.time() - time_flag)
        time_flag = time.time()

    # Serialize to JSON with the enhanced encoder
    json_data = json.loads(json.dumps(actual_routes, cls=EnhancedJSONEncoder))


    # renaming the keys (cant do it in dataclass definition because the 'from' word clashes with the python keyword)
    for route in json_data:
        for trip in route['route']:
            trip['from'] = trip.pop('departure')
            trip['to'] = trip.pop('destination')
            trip['merchandise'] = trip.pop('merchandise')

    # create new file with the Driver objects and the hidden routes
    try:
        create_file = open(f"{data_path}/{size_dataset}/actual.json", "x")
        create_file.close()
    except FileExistsError:
        print("File already exists")

    try:
        with open(f"{data_path}/{size_dataset}/actual.json", "w") as file:
            json.dump(json_data, file, indent=2)
    except FileNotFoundError:
        print("File not found")
        exit(1)

    if DEBUG:
        print("actual routes dumped in file in time: ", time.time() - time_flag)
        time_flag = time.time()

    #get the parameters of the problem
    params = get_parameters()


    # also print the length actual_routes_num and std_routes_num in the same file
    params["actual_routes_num"] = len(actual_routes)
    params["std_routes_num"] = len(route_list)

    # print the parameters of the problem in a json file in the data folder
    try:
        create_file = open(f"{data_path}/{size_dataset}/parameters.json", "x")
        create_file.close()
    except FileExistsError:
        pass


    try:
        with open(f"{data_path}/{size_dataset}/parameters.json", "w") as file:
            json.dump(params, file, indent=2)
    except FileNotFoundError:
        print("File not found")
        exit(1)

    # stop timer
    end = time.time()
    print(f"Time elapsed: {end - start} seconds")


#    p = 0.9
#    mut_bitmap = [1 if random.random() < p else 0 for _ in range(act_routes_num)]

#    for rt, sample in enumerate(mut_bitmap):
#        #have to pick one standard route and add noise into its implementation, i.e. driver could change the endpoints of a trip
#        #(by adding a city, so adding a trip, or by omitting a trip, thus skipping a city), change the quantity of items and even the item types (by omitting some of them or adding some random item types).
#        if sample != 0:
#            std_route = json_data[i] #standard route from which this route is implemented


#            ActualRoute(f"a{rt}", driver, sroute, route)

#        else: continue
    

