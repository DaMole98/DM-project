"""
this file contains the distance metrics used in the solver
"""
import json
import sys

import numpy as np

from sklearn.metrics.pairwise import cosine_similarity

output_path = "./Output/"

MAX_MINIMAL_DISTANCE = 10
FACTORIAL_NEIGHBORHOOD = 5
DEBUG = False
DEBUG_2 = False

from math import floor
from random import randint, seed, sample

from src.Class_Structures.ClassesDefinition import *
from src.Data_Generator.Parameters.parameters import *

def trip_distance(trip1, trip2):
    """
    This function calculates the distance between two trips.

    :param trip1: A Trip object representing the first trip.\n
    :param trip2: A Trip object representing the second trip.\n

    :return: An integer representing the distance between the two trips.\n

    **Algorithm**:\n
    1. Calculate Jaccard Similarity:
        - Calculate the Jaccard similarity (jaccard_similarity) between the two list of cities.\n

    2. Calculate Cosine Distance:
        - Calculate the cosine distance (cosine_distance) between the two list of items.\n

    3. Calculate Distance:
        - Calculate the distance (distance) between the two trips as a linear combination of the Jaccard similarity and the cosine distance.\n
        - Return the distance.\n

    **References**:\n
    - https://en.wikipedia.org/wiki/Jaccard_index\n
    - https://en.wikipedia.org/wiki/Cosine_similarity\n
    """
    # transform in set trip1.departure and trip1.destination
    # calculate the jaccard similarity between the two sets
    # the jaccard similarity is calculated as follows:
    # jaccard_similarity = |A ∩ B| / |A ∪ B|
    # where A and B are the two sets
    # |A ∩ B| is the cardinality of the intersection between A and B
    # |A ∪ B| is the cardinality of the union between A and B
    # the jaccard similarity is then multiplied by 10 to obtain a value in range [0,10]

    # create two Trip objects with the same departure and destination cities
    # the first trip has the items of trip1
    # the second trip has the items of trip2
    Trips = []

    for trip in trip1, trip2:
        try:
            Trips.append(Trip(trip["departure"], trip["destination"], trip["merchandise"]))
        except KeyError:
            Trips.append(Trip(trip["from"], trip["to"], trip["merchandise"]))


    trip1 = Trips[0]
    trip2 = Trips[1]

    # Create sets for the (departure, destination) pairs
    set1 = set((trip1.departure, trip1.destination))
    set2 = set((trip2.departure, trip2.destination))

    # Calculate Jaccard distance
    jaccard_distance = 1 - len(set1.intersection(set2)) / len(set1.union(set2))
    if DEBUG:
        print(f"Jaccard distance: {jaccard_distance}")

    if DEBUG_2:
        print(f"Trip1: {trip1}")
        print(f"Trip2: {trip2}")

    # sort the items in the two trips
    trip1.merchandise = {k: v for k, v in sorted(trip1.merchandise.items(), key=lambda item: item[0])}
    trip2.merchandise = {k: v for k, v in sorted(trip2.merchandise.items(), key=lambda item: item[0])}

    if DEBUG_2:
        print(f"Trip1: {trip1}")
        print(f"Trip2: {trip2}")

    # Combine merchandise dictionaries and extract quantities for all items
    all_items = set(trip1.merchandise.keys()) | set(trip2.merchandise.keys())

    # Extract quantities for all items (set to zero if not present)
    vector1 = np.array([trip1.merchandise.get(item, 0) for item in all_items])
    vector2 = np.array([trip2.merchandise.get(item, 0) for item in all_items])

    # Calculate cosine similarity
    similarity_matrix = cosine_similarity([vector1], [vector2])

    cosine_sim = similarity_matrix[0, 0]

    if cosine_sim < 0:
        cosine_sim = 0.0
    if cosine_sim > 1:
        cosine_sim = 1.0

    if DEBUG:
        print(f"Cosine similarity: {cosine_sim}")

    # Since you want distance, subtract from 1 (cosine distance is 1 - cosine similarity)
    cosine_distance = 1 - cosine_sim

    # the distance between the two trips is calculated as a linear combination in range [0,10]
    # the linear combination is calculated as follows:
    # 0.5 * Jaccard similarity + 0.5 * cosine distance
    # the result is then multiplied by 10 to obtain a value in range [0,10]
    distance = (0.5 * jaccard_distance + 0.5 * cosine_distance) * 10

    # round distance to the 4 decimal digits
    distance = round(distance, 4)

    if DEBUG:
        print(f"Distance: {distance}")
    return distance

# function that calculates the distance between two routes
def route_distance(route1, route2):
    """
    This function calculates the distance between two routes.

    :param route1: A list of Trip objects representing the first route.\n
    :param route2: A list of Trip objects representing the second route.\n

    :return: An integer representing the distance between the two routes.\n

    **Algorithm**:\n
    1. Initialize Distance:
        - Initialize the distance (dist) to 0.\n
    2. For Each Trip in Route1:
        - For each trip (trip1) in route1:
            - Initialize the minimum distance (min_dist) to MAX_MINIMAL_DISTANCE.\n
            - For each trip (trip2) in route2 neighboorhood:
                - Calculate the distance (local_dist) between trip1 and trip2.\n
                - If local_dist is less than min_dist:
                    - Update min_dist to local_dist.\n
            - Add min_dist to dist.\n
    3. Return Distance:
        - Return the average distance between the two routes.\n

    **References**:\n
    - https://en.wikipedia.org/wiki/Jaccard_index\n
    - https://en.wikipedia.org/wiki/Cosine_similarity\n
    """

    tot_dist = 0

    # for each trip in route1 confront it with the corresponding neighboorhood in route2
    # take the minimum distance between the two trips and add it to the total distance
    for index in range(0,len(route1)-1):
        neig_list = floor(len(route2)/FACTORIAL_NEIGHBORHOOD)
        if neig_list == 0:
            neig_list = 1
        min_dist = MAX_MINIMAL_DISTANCE
        if DEBUG:
            print(f"Trip {index} of route1")
        if index - neig_list < len(route2):
            for i in range(max(0, index-neig_list), min(len(route2)-1, index+neig_list)):
                try:
                    local_dist = trip_distance(route1[index], route2[i])
                except IndexError:
                    print(f"IndexError: {i}\n\n")
                    local_dist = trip_distance(route1[index], route2[i-1])
                if local_dist < min_dist:
                    if DEBUG:
                        print(f"local_dist: {local_dist}")
                        print(f"min_dist: {min_dist}")
                    min_dist = local_dist

        tot_dist += min_dist
        if DEBUG:
            print(f"Total distance: {tot_dist}")

    # return the average distance between the two routes
    try:
        return tot_dist / len(route1)
    except ZeroDivisionError:
        return MAX_MINIMAL_DISTANCE

def CheatDistance():
    # calculate the distance between the route in hidden route and the route in probable_hidden_route in average

    # load the hidden routes
    try:
        with open(f"{data_path}HiddenRoutes.json", 'r') as file:
            hidden_routes = json.load(file)

        # make hidden_routes a list of HiddenRoute objects
        hidden_routes = [HiddenRoute(route["dr_id"], route["length"], route["route"]) for route in hidden_routes]
    except FileNotFoundError:
        print("HiddenRoutes.json not found. Please run input_dataset_generator.py first")
        sys.exit()


    # load the probable hidden routes
    try:
        with open(f"{output_path}ProbableHiddenRoutes.json", 'r') as file:
            probable_hidden_routes = json.load(file)

        # make probable_hidden_routes a list of HiddenRoute objects
        probable_hidden_routes = [HiddenRoute(route["dr_id"], route["length"], route["route"]) for route in probable_hidden_routes]
    except FileNotFoundError:
        print("ProbableHiddenRoute.json not found. Please run HiddenRouteFinder.py first")
        sys.exit()

    # calculate the distance between the route in hidden route and the route in probable_hidden_route in average
    avg_dist = 0
    count = 0
    for route in hidden_routes:
        # find the corresponding probable_hidden_route keys ar ids
        for hd_route in probable_hidden_routes:
            if route.dr_id == hd_route.dr_id:
                if DEBUG:
                    print(f"Rider {route.dr_id}")
                avg_dist += min(route_distance(route.route, hd_route.route), route_distance(route.route, hd_route.route))
                # avg_dist += route_distance(route.route, route.route)

                if DEBUG:
                    print(f"Distance between the hidden route and the probable hidden route: {route_distance(route.route, route.route)}")
                count += 1
                break
    avg_dist /= count

    # print the average distance
    print(f"The average distance between the hidden routes and the probable hidden routes is {avg_dist}")

    # return the average distance
    return avg_dist