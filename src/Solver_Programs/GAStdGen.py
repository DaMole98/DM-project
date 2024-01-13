"""
this file contains the solution program for the first tasks in the project
"""

import json
import sys
import time
from random import random, choice, randint, sample

import src.Solver_Programs.DistanceMetrics
from src.Class_Structures.ClassesDefinition import Trip
from src.Data_Generator.Parameters.parameters import data_path
from src.Solver_Programs.DistanceMetrics import getRouteDistance

MAX_ITEM_QUANTITY = 100


def fitnessFunction(route, RouteSample):
    # this function calculates the fitness of a route in terms of average distance from all other route in the sample
    # route is a list of trips
    # RouteSample is a list of routes
    tot_dist = 0
    for rtSam in RouteSample:

        tot_dist += src.Solver_Programs.DistanceMetrics.getRouteDistance(route, rtSam)

    fitness_score = 1/(1+(tot_dist/len(RouteSample)))

    return fitness_score

def mutate(route, mutationRate, cities, items):
    """
    **Description**:
    This function performs mutation on a route.

    :param route: The route to be mutated.
    :type route: list
    :param mutationRate: The probability of mutation.
    :type mutationRate: float
    :param cities: The list of cities that can be included in the routes.
    :type cities: list
    :param items: The list of items that can be associated with trips.
    :type items: list

    :return: The mutated route.
    :rtype: list

    **Algorithm**:\n
    1. Set the probability of changing cities to 0.5.\n
    2. Set the probability of changing items to 0.5.\n
    3. For each trip in the route:
         - Check if mutation should be applied to the current trip, with a certain probability.
            - Change departure city with a certain probability.\n
            - Change destination city with a certain probability.\n
            - Change quantities of items with a certain probability.\n
            - Add new items with random quantities if not present in the trip, with a certain probability.\n
    4. Return the mutated route.
    """
    lamda_0 = 0.5  # Probability of changing cities
    lamda_1 = 0.5  # Probability of changing items

    mutated_route = []

    for trip in route:
        # Check if mutation should be applied to the current trip
        if random() < mutationRate:
            # Change departure city with a certain probability
            if random() < lamda_0:
                trip.departure = choice(cities)

            # Change destination city with a certain probability
            if random() < lamda_0:
                trip.destination = choice(cities)

            # Change quantities of items with a certain probability
            if random() < lamda_1:
                for item in trip.merchandise:
                    if trip.merchandise[item] > 0:
                        trip.merchandise[item] = 0
                    else:
                        trip.merchandise[item] = randint(0, MAX_ITEM_QUANTITY)

                # Add new items with random quantities if not present in the trip
                for item in items:
                    if item not in trip.merchandise:
                        if random() < 0.5:
                            trip.merchandise[item] = randint(0, MAX_ITEM_QUANTITY)

                # Remove items with 0 quantity
                for item in list(trip.merchandise):
                    if trip.merchandise[item] == 0:
                        del trip.merchandise[item]

        mutated_route.append(trip)

    return mutated_route

def crossover(route1, route2):
    """
    **Description**:
    This function performs crossover between two routes.

    :param route1: The first route.
    :type route1: list
    :param route2: The second route.
    :type route2: list

    :return: The two children created by crossover.
    :rtype: tuple

    **Algorithm**:\n
    1. Randomly select a crossover point.\n
    2. Create children by combining trips from parents.\n
    3. Return the children.

    """
    # Randomly select a crossover point
    crossover_point = randint(0, min(len(route1), len(route2)) - 1)

    # Create children by combining trips from parents
    child1 = route1[:crossover_point] + route2[crossover_point:]
    child2 = route2[:crossover_point] + route1[crossover_point:]

    return child1, child2

def initPopulation(popSize, std_routes, cities, items):
    """
    **Description**:
    This function initializes the population of routes.

    :param popSize: The size of the population.
    :type popSize: int
    :param std_routes: The standard routes to be used as a starting point.
    :type std_routes: list
    :param cities: The list of cities that can be included in the routes.
    :type cities: list
    :param items: The list of items that can be associated with trips.
    :type items: list
    :return: The initialized population.
    :rtype: list
    """
    # Initialize an empty population
    population = []

    # change std_routes from list of StandardRoute objects to list of lists of Trip objects
    for _ in range(popSize):
        route = choice(std_routes)
        new_route = []
        for trip in route["route"]:
            new_route.append(Trip(trip["from"], trip["to"], trip["merchandise"]))
        population.append(new_route)

    # Generate routes for the population
    for i in range(popSize):
        # Choose a random standard route and apply mutation
        population[i] = mutate(population[i], 1, cities, items)

    return population


def IsConverged(fitness_scores):
    """
    **Description**:
    This function checks if the algorithm has converged.

    :param fitness_scores: The fitness scores of the current population.
    :type fitness_scores: list

    :return: True if the algorithm has converged, False otherwise.
    :rtype: bool

    **Algorithm**:\n
    1. Set the convergence threshold to 0.9.\n
    2. Check if the maximum fitness score surpasses the convergence threshold.\n
    3. Return the result.

    """
    threshold = 0.999

    # Check if the maximum fitness score surpasses the convergence threshold
    if max(fitness_scores) > threshold:
        return True
    else:
        return False


def geneticAlgorithm(RouteSample, DEBUG, generations=5, popSize=10, mutationRate=0.01, eliteSize=5):
    """
    **Description**:
    This function implements the Genetic Algorithm for Route Optimization.

    :param RouteSample: A sample route to define the structure of routes.
    :type RouteSample: list
    :param generations: The number of generations to run the algorithm for.
    :type generations: int
    :param popSize: The size of the population.
    :type popSize: int
    :param mutationRate: The probability of mutation.
    :type mutationRate: float
    :param eliteSize: The number of elite routes to be preserved in each generation.
    :type eliteSize: int

    :return: The best route found by the algorithm.
    :rtype: list


    **Algorithm**:\n
    1. Load standard routes, cities, and items from JSON files.\n
    2. Initialize the population.\n
    3. For each generation:\n
       - Calculate the fitness of each route in the population.\n
       - Check for convergence.\n
       - Select the elite routes.\n
       - Generate new routes through crossover.\n
       - Mutate the population.\n
    4. Return the best route.

    """
    if DEBUG:
        print("geneticAlgorithm function called")
        global DEBUG_local
        DEBUG_local = 0

    # Load standard routes, cities, and items from JSON files
    try:
        with open(f"{data_path}StandardRoute.json", 'r') as file:
            std_routes = json.load(file)
    except FileNotFoundError:
        print("StandardRoute.json not found. Please run input_dataset_generator.py first")
        sys.exit()

    try:
        with open(f"{data_path}/dev_data/cities.json", 'r') as file:
            cities = json.load(file)
    except FileNotFoundError:
        print("cities.json not found. Please run input_dataset_generator.py first")
        sys.exit()

    try:
        with open(f"{data_path}/dev_data/items.json", 'r') as file:
            items = json.load(file)
    except FileNotFoundError:
        print("items.json not found. Please run input_dataset_generator.py first")
        sys.exit()

    flagConverged = False

    # Initialize the population
    population = initPopulation(popSize, std_routes, cities, items)

    for generation in range(generations):
        if DEBUG:
            print(f"Generation {generation+1} of {generations}")
            print(f"calculating fitness scores")



        # Calculate the fitness of each route in the population
        fitness_scores = [fitnessFunction(route, RouteSample) for route in population]
        print("fitness score computed")


        # Check for convergence
        if IsConverged(fitness_scores):
            flagConverged = True
            if DEBUG:
                print("Converged")
                print(f"Fitness scores: {fitness_scores}")
            break

        # Select the elite routes
        elite = [population[fitness_scores.index(max(fitness_scores))] for _ in range(eliteSize)]
        population = elite

        # Generate new routes through crossover
        for _ in range(popSize - len(elite)):
            # Select two random routes from the elite
            parent1, parent2 = sample(elite, 2)
            # Crossover the two parents
            child1, child2 = crossover(parent1, parent2)
            # Add the two children to the population
            population.append(child1)
            population.append(child2)

        # Mutate the population
        for i in range(len(population)):
            population[i] = mutate(population[i], mutationRate, cities, items)

    # If not converged, evaluate fitness for the final population
    if not flagConverged:
        fitness_scores = [fitnessFunction(route, RouteSample) for route in population]

    # Return the best route
    return population[fitness_scores.index(max(fitness_scores))]
