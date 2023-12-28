"""
this is the main solver program
"""
import dataclasses
import json
import os
import sys
from random import randint, seed, sample

from src.Class_Structures.ClassesDefinition import *
from src.Data_Generator.Parameters.parameters import *
from src.Data_Generator.input_dataset_generator import EnhancedJSONEncoder
from src.Solver_Programs.HiddenRouteFinder import hidden_route_finder
from src.Solver_Programs.recomendationUnit import find_best

output_path = "./Output/"

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

    # load the std_routes
    try:
        with open(f"{data_path}StandardRoute.json", 'r') as file:
            std_routes = json.load(file)

        # make std_routes a list of StandardRoute objects
        # std_routes = [StandardRoute(route["id"], route["route"]) for route in std_routes]
    except FileNotFoundError:
        print("StandardRoute.json not found. Please run input_dataset_generator.py first")
        sys.exit()

    # load the actual_routes
    try:
        with open(f"{data_path}ActualRoutes.json", 'r') as file:
            actual_routes = json.load(file)

        # make actual_routes a list of ActualRoute objects
        # actual_routes = [ActualRoute(route["id"], route["driver"],route["sroute"], route["route"]) for route in actual_routes]
    except FileNotFoundError:
        print("ActualRoute.json not found. Please run input_dataset_generator.py first")
        sys.exit()

    # load the drivers
    try:
        with open(f"{dev_data_path}drivers.json", 'r') as file:
            drivers = json.load(file)

        # make drivers a list of strings
        drivers = [dr for dr in drivers]
    except FileNotFoundError:
        print("Drivers.json not found. Please run input_dataset_generator.py first")
        sys.exit()

    # create a list of HiddenRoute objects
    hidden_routes = []

    for driver in drivers:
        # find the subset of actual routes implemented by the driver
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
        file = open(f"{output_path}ProbableHiddenRoutes.json", 'x')
        file.close()
    except FileExistsError:
        pass

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
        with open(f"{output_path}ProbableHiddenRoutes.json", 'w') as file:
            json.dump(json_data, file, indent=2)
    except FileNotFoundError:
        print("Output folder not found. Please create it first")
        sys.exit()


DEBUG = False

if __name__ == "__main__":
    # perfectRoutesFinder()
    if (DEBUG):
        print("DEBUG is true, so we will find the best rist five routes from the original routes")
    find_best(True)
