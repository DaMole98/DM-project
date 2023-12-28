"""
this file contains the solution program for the second tasks in the project
"""
import json
import sys

from src.Data_Generator.Parameters.parameters import data_path
from src.Solver_Programs.DistanceMetrics import route_distance

DEBUG = 1


def find_best_five_routes(hd_route, list_of_routes):
    """
    this function finds the best five routes from the list of routes
    """
    hd_route = hd_route["route"]
    # use distance in ./DistanceMetrics as the metric to find the best five routes
    dict_of_routes_dist = {}
    for route in list_of_routes:
        dict_of_routes_dist[route["id"]] = route_distance(hd_route, route["route"])

    # sort the dict_of_routes_dist by value in ascending order
    sorted_dict_of_routes_dist = sorted(dict_of_routes_dist.items(), key=lambda x: x[1])

    # return the first five routes
    return sorted_dict_of_routes_dist[:5]


def find_best(original_flag, output_path="./Output/"):
    list_of_routes = []

    if original_flag:
        if(DEBUG):
            print("original flag is true, so we will find the best rist five routes from the original routes")
        try:
            with open(f"{data_path}StandardRoute.json", 'r') as file:
                std_routes = json.load(file)
        except FileNotFoundError:
            print("StandardRoute.json not found. Please run input_dataset_generator.py first")
            sys.exit()
        for route in std_routes:
            list_of_routes.append(route)

    else:
        # TODO: not yet implemented
        # if(DEBUG):
        #     print("original flag is false, so we will find the best rist five routes from the new generated routes")
        # try:
        #     with open(f"{data_path}ProbableHiddenRoutes.json", 'r') as file:
        #         hidden_routes = json.load(file)
        # except FileNotFoundError:
        #     print("ProbableHiddenRoutes.json not found. Please run input_dataset_generator.py first")
        #     sys.exit()
        # for route in hidden_routes:
        #     list_of_routes.append(route["route"])
        print("not yet implemented")
        return False

    # load probable hidden routes
    try:
        with open(f"{output_path}ProbableHiddenRoutes.json", 'r') as file:
            hidden_routes = json.load(file)
    except FileNotFoundError:
        print("ProbableHiddenRoutes.json not found. Please run input_dataset_generator.py first")
        sys.exit()

    if DEBUG:
        print(f"len of hidden_routes: {len(hidden_routes)}")
        print(f"len of list_of_routes: {len(list_of_routes)}")

    # create a dictionary of drivers and their best five routes
    drivers_association = {}

    # for each probable hidden route, find the best five routes
    for route in hidden_routes:
        # find the best five routes
        if DEBUG:
            print(f"driver: {route['dr_id']}")
        best_five_routes = find_best_five_routes(route, list_of_routes)

        # add only the ids of the best five routes to the dictionary
        drivers_association[route["dr_id"]] = [route[0] for route in best_five_routes]
        if DEBUG:
            print(f"best five routes: {drivers_association[route['dr_id']]}")



    # create a JSON file called drivers.json in this format
    # [
    #     {driver:A, routes:[s1, s2, s3, s4, s5]},
    #     {driver:B, routes:[s1, s2, s3, s4, s5]},
    # ...
    # ]
    # where s1, s2, s3, s4, s5 are the best five routes for the driver
    try:
        with open(f"{output_path}drivers.json", 'w') as file:
            json.dump(drivers_association, file, indent=4)
        if DEBUG:
            print("drivers.json created in path: " + output_path)
            print(drivers_association)
    except FileNotFoundError:
        print("drivers.json not found. Please run input_dataset_generator.py first")
        sys.exit()
