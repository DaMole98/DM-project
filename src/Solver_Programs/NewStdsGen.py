"""
this file is used to generate new standards for the solver, in the first task of the project
"""

import json
import os
import sys
import time
from dataclasses import dataclass
from random import randint, sample, seed

from src.Class_Structures.ClassesDefinition import StandardRoute, Trip, Driver
from src.Data_Generator.input_dataset_generator import EnhancedJSONEncoder
from src.Solver_Programs.GAStdGen import geneticAlgorithm

output_path = "./Output/"


# function that generates K new standards routes
def generate_new_std(K, samplesChoice, DEBUG):

    if DEBUG:
        print("generate_new_std function called")
        print(f"K = {K}")
        print(f"samplesChoice = {samplesChoice}")

    # load probable hidden routes
    try:
        with open(f"{output_path}ProbableHiddenRoutes.json", 'r') as file:
            hidden_routes = json.load(file)
    except FileNotFoundError:
        print("ProbableHiddenRoutes.json not found. Please run input_dataset_generator.py first")
        sys.exit()

    perfRoutes = []

    # change hidden_routes from list of HiddenRoute objects to list of lists of Trip objects
    for route in hidden_routes:
        new_route = []
        for trip in route["route"]:
            try:
                new_route.append(Trip(trip["from"], trip["to"], trip["merchandise"]))
            except KeyError:
                print("Error: missing key in trip")
                exit(1)
        perfRoutes.append(new_route)

    newStd = []
    len_sample = len(hidden_routes)/K
    if len_sample < 5:
        len_sample = 5
    if samplesChoice == 0:
        # random sampling of K sets of routes
        for i in range(K):
            RouteSample = sample(perfRoutes, int(len_sample))
            # print(RouteSample)
            print(f"round k:{i}")
            newStd.append(geneticAlgorithm(RouteSample, DEBUG))

    else:
        pass

    if DEBUG:
        print("newStd:")
        for route in newStd:
            print(f"{route}")

    PrintStd = []

    # change the format of Trips to the format of the Trips in the original dataset [from, to, merchandise]
    count = 0
    for route in newStd:
        new_route = []
        for trip in route:
            newtrip = {}
            newtrip["from"] = trip.departure
            newtrip["to"] = trip.destination
            newtrip["merchandise"] = trip.merchandise
            new_route.append(newtrip)
        PrintStd.append( {"id": f"s{count}", "route": new_route})
        count += 1

    print(PrintStd)
    # Serialize to JSON with the enhanced encoder
    json_data = json.loads(json.dumps(PrintStd, cls=EnhancedJSONEncoder))

    # create new file json called recStandard.json
    try:
        create_file = open(f"{output_path}recStandard.json", "x")
        create_file.close()
    except FileExistsError:
        pass

    try:
        with open(f"{output_path}recStandard.json", "w") as file:
            json.dump(json_data, file, indent=2)
    except FileNotFoundError:
        print("File not found")
        exit(1)