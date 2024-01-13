"""
this file is used to generate new standards for the solver, in the first task of the project
"""

import json
import os
import sys
import time
from dataclasses import dataclass
from random import randint, sample, seed

from src.Class_Structures.ClassesDefinition import StandardRoute, Trip, Driver, ActualRoute
from src.Data_Generator.Parameters.parameters import data_path, size_dataset
from src.Data_Generator.input_dataset_generator import EnhancedJSONEncoder
from src.Solver_Programs.DistanceMetrics import getRouteDistance
from src.Solver_Programs.GAStdGen import geneticAlgorithm
from src.Solver_Programs.recommenderClustering import cluster_routes

output_path = "./Output/"

'''
# function that generates K new standards routes
def clusterApproach(RouteSet, K, DEBUG):
    """
    This function generates K new standards routes using the cluster approach.

    :param perfRoutes:
    :param K:
    :param DEBUG:
    :return:
    """
    def hashFunction(index, route):
        """
        This function generates a hash function that returns the distance between the route and a random route in actualRoutes
        """

        return getRouteDistance(route, sample_routes[index])

    # creation of M hashing function, each hash function will return the distance between the route and a random route in actualRoutes
    # sample M routes from ../../data/acutalRoutes.json
    # M = 10
    M = 5

    # load actual routes
    try:
        with open(f"{data_path}ActualRoutes.json", 'r') as file:
            actual_routes = json.load(file)
    except FileNotFoundError:
        print("ActualRoute.json not found. Please run input_dataset_generator.py first")
        sys.exit()


    # sample M routes from actual_routes
    sample_routes = sample(actual_routes, M)

    # make sample_routes a list of list of Trip objects
    sample_routes = [[Trip(trip["from"], trip["to"], trip["merchandise"]) for trip in route["route"]] for route in sample_routes]


    routes_hash = []

    # for each route in RouteSet, calculate the hash value and store it in routes_hash as index_route: [hash_value_1, hash_value_2, ...]
    for route in RouteSet:
        hash_values = []
        for i in range(M):
            hash_values.append(hashFunction(i, route))
        routes_hash.append(hash_values)

    for route in RouteSet:
        print(f"route: {route}")

    for route in sample_routes:
        print(f"sample route: {route}")

    for route in routes_hash:
        print(f"route hash: {route}")




    pass
'''


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
    len_sample = len(hidden_routes) / K
    if len_sample < 5:
        len_sample = 5
    if samplesChoice == 0:
        # random sampling of K sets of routes
        for i in range(K):
            RouteSample = sample(perfRoutes, int(len_sample))
            # print(RouteSample)
            print(f"round k:{i}")
            newStd.append(geneticAlgorithm(RouteSample, DEBUG))

    elif samplesChoice == 1:
        std_obj = []
        act_obj = []
        print(f"{data_path}{size_dataset}_dataset/actual.json")
        try:
            with open(f"{data_path}{size_dataset}_dataset/actual.json", 'r') as file:
                actuals = json.load(file)
                for act in actuals:
                    act_obj.append(ActualRoute(id=act['id'], driver=act['driver'], sroute=act['sroute'],
                                               route=[Trip(tr['from'], tr['to'], tr['merchandise']) for tr in
                                                      act['route']]))
        except FileNotFoundError:
            print("actuals.json not found. Please run input_dataset_generator.py first")
            sys.exit(1)

        try:
            with open(f"{data_path}{size_dataset}_dataset/standard.json", 'r') as file:
                stds = json.load(file)
                for std in stds:
                    std_obj.append(StandardRoute(std['id'],
                                                 [Trip(tr['from'], tr['to'], tr['merchandise']) for tr in
                                                  std['route']]))
        except FileNotFoundError:
            print("standard.json not found. Please run input_dataset_generator.py first")
            sys.exit(1)

        clusters = cluster_routes(std_routes=std_obj, actual_routes=act_obj, clusters=K)
        clusters.sort(key=lambda x: x[1])
        #clusters = sorted(clusters, key=lambda x: x[1])
        #print([cl[1] for cl in clusters])
        # route_sample = []
        i = 0
        cnk = []
        while i < len(clusters):
            if len(cnk) == 0 or clusters[i][1] == clusters[i - 1][1]:
                cnk.append(clusters[i][0])
            else:
                # run algorithm
                adapted_routes = []
                cnk = sample(cnk, 5)
                for actual_obj in cnk:
                    adapted_routes.append(actual_obj.route)

                newStd.append(geneticAlgorithm(adapted_routes, DEBUG))
                cnk.clear()
            i += 1

        ########
        # for i in range(len(clusters)):
    #
    #    RouteSample = clusters[i]
    #    # print(RouteSample)
    #    print(f"round k:{i}")
    #    newStd.append(geneticAlgorithm(RouteSample, DEBUG))
    ########
    else:
        print("Error: samplesChoice must be 0 or 1")
        exit(1)

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
        PrintStd.append({"id": f"s{count}", "route": new_route})
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
