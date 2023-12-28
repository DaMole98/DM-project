"""
this file contains the solution program for the first tasks in the project
"""

import json
import sys


def generateBaseRoute():
    # generate a base route that will be used to generate the hidden routes
    # we can use the greedy algorithm to generate the route
    pass



def generateFromSample(hiddenRouteSample):
    # in input we have the sample of the hidden routes
    # we have to generate a route that minimizes the distance from all the routes in the sample
    # we can use route_distance from ./DistanceMetrics.py to calculate the distance between two routes
    # we can use the genetic algorithm to generate the route

    # ROUTE are list of TRIPS
    # TRIPS are the class defined in ClassesDefinition.py

    # implement genetic algorithm for the problem
    BaseRoute = []
    BaseRoute = generateBaseRoute()