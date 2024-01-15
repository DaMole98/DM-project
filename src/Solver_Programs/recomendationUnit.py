"""
this file contains the solution program for the second tasks in the project
"""
import json
import math
import sys
from math import floor

from src.Class_Structures.ClassesDefinition import Trip
from src.Solver_Programs.DistanceMetrics import getRouteDistance
from src.Solver_Programs.plotVisualizer import plotUtilityMatrix


def find_best_five_routes(hd_route, list_of_routes):
    """
    this function finds the best five routes from the list of routes using content based recommendation, using content based recommendation approach
    :param hd_route: the hidden route
    :param list_of_routes: the list of routes

    **Algorithm**
    1. convert the hd_route and each route in the list_of_routes to a list of Trip objects
    2. use the getRouteDistance function in ./DistanceMetrics to find the distance between the hd_route and each route in the list_of_routes
    3. sort the list_of_routes by distance in ascending order
    4. return the first five routes
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


def find_best(original_flag, data_path, DEBUG, output_path="./results/"):
    list_of_routes = []
    s_routes = []
    a_routes = []

    if original_flag:
        if DEBUG:
            print("original flag is true, so we will find the best rist five routes from the original routes")
        try:
            with open(f"{data_path}standard.json", 'r') as file:
                std_routes = json.load(file)
        except FileNotFoundError:
            print("standard.json not found. Please run input_dataset_generator.py first")
            sys.exit()
    else:
        # load the new std_routes from ./results/recStandard.json
        if DEBUG:
            print("original flag is false, so we will find the best rist five routes from the new routes")
        try:
            with open(f"{output_path}recStandard.json", 'r') as file:
                std_routes = json.load(file)
        except FileNotFoundError:
            print("recStandard.json not found. Please run input_dataset_generator.py first")
            sys.exit()

    for route in std_routes:
        s_routes.append({
            "id": route["id"],
            "route": [Trip(trip["from"], trip["to"], trip["merchandise"]) for trip in route["route"]]
        })

    # load actual routes
    try:
        with open(f"{data_path}actual.json", 'r') as file:
            actual_routes = json.load(file)
    except FileNotFoundError:
        print("actual.json not found. Please run input_dataset_generator.py first")
        sys.exit()

    for route in actual_routes:
        a_routes.append({
            "id": route["id"],
            "driver": route["driver"],
            "sroute": route["sroute"],
            "route": [Trip(trip["from"], trip["to"], trip["merchandise"]) for trip in route["route"]]
        })

    # if DEBUG:
    #     print(f"data loaded from {data_path}actual.json")
    #     for route in actual_routes:
    #         print(f"route: {route}")

    size = data_path.split("/")[-2]



    # load probable hidden routes
    try:
        with open(f"{output_path}perfectRoute.json", 'r') as file:
            hidden_routes = json.load(file)
    except FileNotFoundError:
        print("perfectRoute.json not found. Please run input_dataset_generator.py first")
        sys.exit()

    if DEBUG:
        print(f"len of hidden_routes: {len(hidden_routes)}")
        print(f"len of list_of_routes: {len(list_of_routes)}")

    # create a dictionary of drivers and their best five routes
    drivers_association = {}

    if original_flag:
        # create a dictionary of drivers and their best five routes
        drivers_association =  new_recfunc(s_routes, a_routes, [], DEBUG, original_flag, size)
    else:
        # for each probable hidden route, find the best five routes
        for route in hidden_routes:
            # find the best five routes
            if DEBUG:
                print(f"driver: {route['driver']}")
            best_five_routes = find_best_five_routes(route, list_of_routes)

            # add only the ids of the best five routes to the dictionary
            drivers_association[route["driver"]] = [route[0] for route in best_five_routes]
            if DEBUG:
                print(f"best five routes: {drivers_association[route['driver']]}")


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


def new_recfunc(std_routes, actual_routes, new_std_routes, DEBUG, flag_original, size):
    """
    this function is the new recommendation function using collaborative filtering approach
    :param std_routes: the standard routes
    :param actual_routes: the actual routes
    :param new_std_routes: the new standard routes (we are not using them)
    :param DEBUG: debug flag
    :param flag_original:  to indicate if we are using the original routes or the new routes
    :return: a dictionary of drivers and their best five routes

    **Algorithm**

    1. create a utility matrix of drivers x std_routes
    2. for each driver, find the n most similar drivers
    3. for each driver, find the best five routes in terms of the utility matrix
    4. create a dictionary of drivers and their best five routes
    5. return the dictionary
    """
    if DEBUG:
        print("new_recfunc function called")
        print(f"data set size: {size}")
        # print(f"new_std_routes: {new_std_routes}")
        # print(f"flag_original: {flag_original}


    utility_matrix = []



    list_of_drivers = []
    for route in actual_routes:
        if route["driver"] not in list_of_drivers:
            list_of_drivers.append(route["driver"])

    # sort list_of_drivers
    list_of_drivers.sort()

    # the matrix is a list of lists with rows as drivers and columns as std_routes
    # the value of each cell is the average distance between the std_route in the column and the actual route of the driver in the row referring to the std_route
    # if a driver didn't take a std_route, the value of the cell is nill
    for i in range(0, len(list_of_drivers)):
        utility_matrix.append([])
        for _ in std_routes:
            utility_matrix[i].append(None)


    if DEBUG:
        count = 0

    for driver in list_of_drivers:
        for route in std_routes:
            count_local = 0
            for actual_route in actual_routes:
                if route["id"] == actual_route["sroute"] and driver == actual_route["driver"]:
                    actual_routes.remove(actual_route)
                    if utility_matrix[list_of_drivers.index(driver)][std_routes.index(route)] is None:
                        utility_matrix[list_of_drivers.index(driver)][std_routes.index(route)] = 0
                    utility_matrix[list_of_drivers.index(driver)][std_routes.index(route)] += 1 - getRouteDistance(route["route"], actual_route["route"])
                    count_local += 1
            if utility_matrix[list_of_drivers.index(driver)][std_routes.index(route)] is not None:
                utility_matrix[list_of_drivers.index(driver)][std_routes.index(route)] /= count_local


    if DEBUG:
        plotUtilityMatrix(utility_matrix, list_of_drivers, f"utility_matrix_{size}_1")
        # exit(1)

    # now find n similar drivers for each driver in terms of the utility matrix
    n = int(round(len(list_of_drivers)/(math.log2(len(list_of_drivers)+1)), 0))
    print (f"n: {n}")

    # create a matrix list_of_drivers x list_of_drivers
    similarity_matrix = []
    for i in range(0, len(list_of_drivers)):
        similarity_matrix.append([])
        for _ in list_of_drivers:
            similarity_matrix[i].append(None)

    # fill the similarity matrix
    for i in range(0, len(list_of_drivers)):
        for j in range(i+1, len(list_of_drivers)):
            similarity_matrix[i][j] = driver_similarity(utility_matrix[i], utility_matrix[j])
            similarity_matrix[j][i] = similarity_matrix[i][j]

    # for each driver, find the n most similar drivers
    # in order to find them we used the KNN algorithm in which we find the n most similar drivers
    similar_drivers = []
    for i in range(0, len(list_of_drivers)):
        similar_drivers.append([])
        for j in range(0, len(list_of_drivers)):
            if j != i:
                similar_drivers[i].append((j, similarity_matrix[i][j]))
        similar_drivers[i].sort(key=lambda x: x[1], reverse=True)
        similar_drivers[i] = similar_drivers[i][:n]


    # fill the utility matrix with the average of the utility of the n most similar drivers
    for i in range(0, len(list_of_drivers)):
        for j in range(0, len(std_routes)):
            if utility_matrix[i][j] is None:
                utility_matrix[i][j] = 0
                count = 0
                for driver in similar_drivers[i]:
                    if utility_matrix[driver[0]][j] is not None:
                        count += 1
                        utility_matrix[i][j] += utility_matrix[driver[0]][j]
                if count != 0:
                    utility_matrix[i][j] /= count

    if DEBUG:
        plotUtilityMatrix(utility_matrix, list_of_drivers, f"utility_matrix_{size}_2")
        # exit(1)

    # for each driver, find the best five routes in terms of the utility matrix
    best_five_routes = []
    for i in range(0, len(list_of_drivers)):
        best_five_routes.append([])
        for j in range(0, len(std_routes)):
            if utility_matrix[i][j] is not None:
                best_five_routes[i].append((j, utility_matrix[i][j]))
                if DEBUG:
                    print(f"driver: {list_of_drivers[i]}, route: {std_routes[j]['id']}, utility: {utility_matrix[i][j]}")
        best_five_routes[i].sort(key=lambda x: x[1], reverse=True)
        best_five_routes[i] = best_five_routes[i][:5]


    # create a dictionary of drivers and their best five routes
    drivers_association = {}

    # add only the ids of the best five routes to the dictionary
    for i in range(0, len(list_of_drivers)):
        drivers_association[list_of_drivers[i]] = [std_routes[route[0]]["id"] for route in best_five_routes[i]]

    return drivers_association




def driver_similarity(d1_row, d2_row):
    # d1_row and d2_row are the rows of the utility matrix for driver d1 and d2 respectively
    # this function returns the similarity between d1 and d2 as cosine similarity

    cosinesim = 0
    d1_norm = 0
    d2_norm = 0
    for i in range(0, len(d1_row)):
        if d1_row[i] is None or d2_row[i] is None:
            continue
        cosinesim += d1_row[i] * d2_row[i]
        d1_norm += d1_row[i] * d1_row[i]
        d2_norm += d2_row[i] * d2_row[i]
    d1_norm = math.sqrt(d1_norm)
    d2_norm = math.sqrt(d2_norm)
    if d1_norm == 0 or d2_norm == 0:
        return 0
    cosinesim /= (d1_norm * d2_norm)

    return cosinesim