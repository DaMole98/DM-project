"""
this file contains the solution program for the second tasks in the project
"""
import json
import sys

from src.Class_Structures.ClassesDefinition import Trip
from src.Data_Generator.Parameters.parameters import data_path
from src.Solver_Programs.DistanceMetrics import getRouteDistance

DEBUG = 1


def find_best_five_routes(hd_route, list_of_routes):
    """
    this function finds the best five routes from the list of routes
    """
    tmp_hd_route = []
    for trip in hd_route["route"]:
        tmp_hd_route.append(Trip(trip["from"], trip["to"], trip["merchandise"]))
    # use distance in ./DistanceMetrics as the metric to find the best five routes
    dict_of_routes_dist = {}
    for route in list_of_routes:
        tmp_route = []
        for trip in route["route"]:
            tmp_route.append(Trip(trip["from"], trip["to"], trip["merchandise"]))
        dict_of_routes_dist[route["id"]] = getRouteDistance(tmp_hd_route, tmp_route)

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
    else:
        # load the new std_routes from ./Output/recStandard.json
        if(DEBUG):
            print("original flag is false, so we will find the best rist five routes from the new routes")
        try:
            with open(f"{output_path}recStandard.json", 'r') as file:
                std_routes = json.load(file)
        except FileNotFoundError:
            print("recStandard.json not found. Please run input_dataset_generator.py first")
            sys.exit()

    for route in std_routes:
        list_of_routes.append(route)

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


    data = []
    for driver in drivers_association:
        data.append({
            "driver": driver,
            "routes": drivers_association[driver]
        })


    # create a JSON file called drivers.json in this format
    # [
    #     {driver:A, routes:[s1, s2, s3, s4, s5]},
    #     {driver:B, routes:[s1, s2, s3, s4, s5]},
    # ...
    # ]
    # where s1, s2, s3, s4, s5 are the best five routes for the driver
    # serialize drivers_association to JSON
    json_object = json.dumps(drivers_association, indent=4)
    try:
        with open(f"{output_path}drivers.json", 'w') as file:
            json.dump(data, file, indent=4)
        if DEBUG:
            print("drivers.json created in path: " + output_path)
            print(drivers_association)
    except FileNotFoundError:
        print("drivers.json not found. Please run input_dataset_generator.py first")
        sys.exit()
