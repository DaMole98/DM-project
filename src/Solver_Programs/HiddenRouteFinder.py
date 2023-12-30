"""
this script is used to find the hidden route for each driver
"""

import json
import os
import sys
from math import floor
from random import randint, seed, sample

DEBUG = False

MIN_INCREMENT = 3
MAX_INCREMENT = 10
PERCENTAGE_INCREMENT = 0.0005

from src.Class_Structures.ClassesDefinition import *
from src.Data_Generator.Parameters.parameters import *

# function that found the hidden route for a driver, given the actual routes and the standard routes he implemented
class Threshold:
    value: 50


def hidden_route_finder(std_routes, actual_routes, driver, FACTORIAL_LIMIT=3):
    """
    This function finds the hidden route for a driver, given the actual routes and the standard routes he implemented.

    :param std_routes: A list of StandardRoute objects representing the standard routes implemented by the driver.\n
    :param actual_routes: A list of ActualRoute objects representing the actual routes implemented by the driver.\n
    :param driver: A string representing the identifier of the driver.\n

    :return: A HiddenRoute object representing the probable hidden route for the driver.\n

    **Algorithm**:\n
    1. Calculate Average Lengths:
        - Calculate the average length of the actual routes (avg_length) and the standard routes (avg_length_s) implemented by the driver.\n

    2. Calculate Difference:
        - Find the difference (diff) between the average length of actual routes and standard routes.\n

    3. Calculate Probable Length:
        - Calculate the probable length of the hidden route (probable_length) by adding the difference to the average length.\n

    4. Round Probable Length:
        - Round probable_length to the nearest integer for practicality.\n

    5. Create Hidden Route Object:
        - Create an instance of the HiddenRoute class (probable_hidden_route) with the driver's identifier and the probable length.\n

    6. Analyze Actual Routes:
        - For each trip (i) in the route:
            - Analyze the (i) trip of each actual route.\n
            - Find the most frequent departure (probable_from) and destination (probable_to) cities.\n

    7. Create Probable Trip:
        - Create a probable trip (probable_trip) with the most frequent departure and destination cities.\n

    8. Determine Merchandise:
        - For each item in actual route:
            - Create a dict (pr_merch) associating each item with the overall quantity of that item and the number of times it appears.\n
            - Calculate the average quantity of each item.\n
            - Round the average quantity to the nearest integer for practicality.\n
            - If an item appears in more than some percentage of the actual routes, add it to the probable trip, in the average quantity.\n

    9. Build Hidden Route:
        - Append the probable trip to the probable_hidden_route\n

    10. Return Result:
        - Return the probable_hidden_route as the output of the function.\n

    Note:\n
    - The function utilizes a few constants, including DEBUG, which can be used for debugging purposes.\n

    **Example Usage:**\n
    result = hidden_route_finder(std_routes, actual_routes, "driver123")\n
    print(result)\n
    """
    #TODO: change the format of the file json because it' wrong
    if DEBUG:
        print(f"Finding hidden route for driver {driver}")

    # find the floor avg length of the actual routes implemented by the driver
    avg_length = 0
    for route in actual_routes:
        avg_length += len(route["route"])

    try :
        avg_length = avg_length / len(actual_routes)
    except ZeroDivisionError:
        return None

    # find the floor avg length of the standard routes implemented by the driver
    avg_length_s = 0
    for route in std_routes:
        avg_length_s += len(route["route"])

    try :
        avg_length_s = avg_length_s / len(std_routes)
    except ZeroDivisionError:
        return None


    # take the diff between the avg length of the actual routes and the avg length of the standard routes
    diff = avg_length - avg_length_s

    probable_length = avg_length + diff

    # round probable_length to the nearest integer
    if probable_length - floor(probable_length) >= 0.5:
        probable_length = floor(probable_length) + 1
    else:
        probable_length = floor(probable_length)

    if DEBUG:
        print(f"Average length of the actual routes implemented by the driver: {avg_length}")
        print(f"Average length of the standard routes implemented by the driver: {avg_length_s}")
        print(f"Diff between the avg length of the actual routes and the avg length of the standard routes: {diff}")
        print(f"Probable length of the hidden route: {probable_length}")


    # create a hidden route object
    probable_hidden_route = HiddenRoute(driver, probable_length, [])
    for i in range(0, probable_length):
        probable_trip = Trip("", "", {})

        probable_from = {}
        probable_to = {}

        # analyze the first trip of each actual route implemented by the driver
        # and find the most frequent from and to cities
        for route in actual_routes:
            if len(route["route"]) > i:
                flag_dep = False
                flag_dest = False

                # find the standard route  associated with the actual route
                for std_route in std_routes:
                    if std_route["id"] == route["sroute"]:
                        try:
                            dep_std = std_route["route"][i]["from"]
                            dest_std = std_route["route"][i]["to"]
                        except IndexError:
                            continue

                if route["route"][i]["from"] == dep_std:
                    flag_dep = True
                if route["route"][i]["to"] == dest_std:
                    flag_dest = True

                    # Process "from" part
                from_location = route["route"][i]["from"]
                if from_location in probable_from:
                    probable_from[from_location] += MIN_INCREMENT if flag_dep else ( MAX_INCREMENT + PERCENTAGE_INCREMENT * probable_from[from_location] )
                else:
                    probable_from[from_location] = MIN_INCREMENT if flag_dep else MAX_INCREMENT

                # Process "to" part
                to_location = route["route"][i]["to"]
                if to_location in probable_to:
                    probable_to[to_location] += MIN_INCREMENT if flag_dest else (MAX_INCREMENT + PERCENTAGE_INCREMENT * probable_to[to_location])
                else:
                    probable_to[to_location] = MIN_INCREMENT if flag_dest else MAX_INCREMENT

        pr_dep = {"city": "", "count": 0}
        pr_dest = {"city": "", "count": 0}
        for city in probable_from:
            if probable_from[city] > pr_dep["count"] or pr_dep == "":
                pr_dep = {"city": city, "count": probable_from[city]}

        for city in probable_to:
            if probable_to[city] > pr_dest["count"] or pr_dest == "":
                pr_dest = {"city": city, "count": probable_to[city]}

        # fill trip object with the most frequent departure and destination cities
        probable_trip.departure = pr_dep["city"]
        probable_trip.destination = pr_dest["city"]

        pr_merch = {}

        # create a dict associating each item with the overall quantity of that item and the number of times it appears
        # a dict like "items": {"item1": {"avg": 2, "count": 3}, "item2": {"avg": 1, "count": 1}}
        count = 0
        for route in actual_routes:
            if len(route["route"]) > i:
                count += 1
                for item in route["route"][i]["merchandise"]:
                    pr_qty = 0
                    if item in pr_merch:
                        pr_merch[item]["avg"] += route["route"][i]["merchandise"][item]
                        pr_merch[item]["count"] += 1
                    else:
                        pr_merch[item] = {"avg": route["route"][i]["merchandise"][item], "count": 1}

        # calculate the average quantity of each item
        for item in pr_merch:
            pr_merch[item]["avg"] = pr_merch[item]["avg"] / pr_merch[item]["count"]
            # round the average quantity to the nearest integer
            if pr_merch[item]["avg"] - floor(pr_merch[item]["avg"]) >= 0.5:
                pr_merch[item]["avg"] = floor(pr_merch[item]["avg"]) + 1
            else:
                pr_merch[item]["avg"] = floor(pr_merch[item]["avg"])

        # fill trip object with the merchandise
        fact = FACTORIAL_LIMIT

        while len(probable_trip.merchandise) < 2 and fact > 1:
            for item in pr_merch:
                # if an item appears in more than some percentage of the actual routes, add it to the probable trip, in the average quantity
                # the percentage is determined by the fact variable that is decremented at each iteration till merchandise has cardinality at least 2
                if pr_merch[item]["avg"] > 0 and pr_merch[item]["count"] > count / fact:
                    probable_trip.merchandise[item] = pr_merch[item]["avg"]
            fact += 1.3

        probable_hidden_route.route.append(probable_trip)

    return probable_hidden_route
