"""
this is the main solver program
"""
import dataclasses
import json
import os
import sys
from random import randint, seed, sample

from src.Class_Structures.ClassesDefinition import *
from src.Data_Generator.input_dataset_generator import EnhancedJSONEncoder
from src.Solver_Programs.HiddenRouteFinder import hidden_route_finder
from src.Solver_Programs.NewStdsGen import generate_new_std
from src.Solver_Programs.recomendationUnit import find_best

output_path = "./Output/"

DEBUG = True

# TODO: check the name and the format of all file before handing in the project
class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)


def perfectRoutesFinder():
    # set entropy to a number as desired to make the results reproducible
    entropy = os.urandom(128)
    seed(entropy)

    if DEBUG:
        print("Loading the routes")
        print(data_path)


    # load the std_routes
    try:
        with open(f"{data_path}standard.json", 'r') as file:
            std_routes = json.load(file)

        # make std_routes a list of StandardRoute objects
        # std_routes = [StandardRoute(route["id"], route["route"]) for route in std_routes]
    except FileNotFoundError:
        print("standard.json not found. Please run input_dataset_generator.py first")
        sys.exit()

    # load the actual_routes
    try:
        with open(f"{data_path}actual.json", 'r') as file:
            actual_routes = json.load(file)

        # make actual_routes a list of ActualRoute objects
        # actual_routes = [ActualRoute(route["id"], route["driver"],route["sroute"], route["route"]) for route in actual_routes]
    except FileNotFoundError:
        print("ActualRoute.json not found. Please run input_dataset_generator.py first")
        sys.exit()

    # # load the drivers
    # try:
    #     with open(f"{dev_data_path}drivers.json", 'r') as file:
    #         drivers = json.load(file)
    #
    #     # make drivers a list of strings
    #     drivers = [dr for dr in drivers]
    # except FileNotFoundError:
    #     print("Drivers.json not found. Please run input_dataset_generator.py first")
    #     sys.exit()

    # create a list of HiddenRoute objects
    hidden_routes = []

    ID_visited = []

    # enumerate the actual_routes
    for i in range(len(actual_routes)):
        # check the ID of the route
        if actual_routes[i]["driver"] not in ID_visited:
            route = actual_routes[i]
            ID_visited.append(route["driver"])
            driver = route["driver"]
            driver_actual_routes = []
            driver_std_routes = []
            for route in actual_routes:
                # print (route["driver"])
                if route["driver"] == driver:
                    driver_actual_routes.append(route)
                for route_s in std_routes:
                    if route_s["id"] == route["sroute"] and route_s not in driver_std_routes:
                        driver_std_routes.append(route_s)

            # find the hidden route for the driver
            hidden_route = hidden_route_finder(driver_std_routes, driver_actual_routes, driver)

            if hidden_route is not None:
                hidden_routes.append(hidden_route)

    # create a JSON file for the hidden routes called ProbableHiddenRoutes.json
    try:
        file = open(f"{output_path}perfectRoute.json", 'x')
        file.close()
    except FileExistsError:
        pass

    # convert the hidden_routes from {id: id,

    json_data = json.loads(json.dumps(hidden_routes, cls=EnhancedJSONEncoder))

    # renaming the keys (cant do it in dataclass definition because the 'from' word clashes with the python keyword)
    for route in json_data:
        for trip in route['route']:
            trip['from'] = trip.pop('departure')
            trip['to'] = trip.pop('destination')
            trip['merchandise'] = trip.pop('merchandise')
            trip['merchandise'] = trip.pop('merchandise')


    # write the hidden routes to a json file
    try:
        with open(f"{output_path}perfectRoute.json", 'w') as file:
            json.dump(json_data, file, indent=2)
    except FileNotFoundError:
        print("Output folder not found. Please create it first")
        sys.exit()




if __name__ == "__main__":
    if DEBUG:
        print("Welcome to the main solver program")

    print("Which dataset do you want to use?")
    print("1. small")
    print("2. medium")
    print("3. large")
    print("4. small1")
    print("5. small2")
    print("6. medium1")

    dataset = int(input("Enter your choice: "))
    if dataset == 1:
        size_dataset = "small"
    elif dataset == 2:
        size_dataset = "medium"
    elif dataset == 3:
        size_dataset = "large"
    elif dataset == 4:
        size_dataset = "small1"
    elif dataset == 5:
        size_dataset = "small2"
    elif dataset == 6:
        size_dataset = "medium1"
    else:
        print("Invalid choice")
        sys.exit()

    size_dataset += "_dataset"

    global data_path
    global dev_data_path
    data_path = f"../../data/{size_dataset}/"
    dev_data_path = f"{data_path}dev_data/"

    if DEBUG:
        print(f"Using {size_dataset} dataset")

    if DEBUG:
        print("Finding the Perfect Routes")

    # start timer
    import time
    start = time.time()
    time_flag = start
    perfectRoutesFinder()
    if DEBUG:
        print(f"Time taken to find the perfect routes: {time.time() - time_flag}")
    time_flag = time.time()

    if DEBUG:
        print("Generating new standard routes")
    # take in input the number of new standard routes to be generated
    K = int(input("Enter the number of new standard routes to be generated: "))

    MAX_K = 500

    if size_dataset.__contains__("small"):
        MAX_K = 10
    elif size_dataset.__contains__("medium"):
        MAX_K = 100

    if K < 0 or K > MAX_K:
        print("Invalid number of routes")
        sys.exit()

    generate_new_std(K, 0, 0)
    if DEBUG:
        print(f"Time taken to generate new standard routes: {time.time() - time_flag}")
    time_flag = time.time()

    if DEBUG:
        print("Finding the best five routes for each driver")
    find_best(0)
    if DEBUG:
        print(f"Time taken to find the best five routes: {time.time() - time_flag}")

    if DEBUG:
        print(f"Total time taken: {time.time() - start}")
        print("Done")
