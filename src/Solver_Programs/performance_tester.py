"""
This scripts plots the performance of the hidden route finder algorithm.
The plots represent the distance between the real hidden routes and the inferred ones
as the number of actual routes implementations for each driver increases
"""
import json
from random import sample
import matplotlib.pyplot as plt

from similarityMeasure import route_similarity
from src.Class_Structures.ClassesDefinition import ActualRoute, Trip, StandardRoute, Driver
from src.Data_Generator.Parameters.parameters import *
from src.Data_Generator.actual_route_generator import generate_actual_route
from src.Data_Generator.hidden_route_generator import generate_hidden_routes
from src.Solver_Programs.DistanceMetrics import route_distance
from src.Solver_Programs.HiddenRouteFinder import hidden_route_finder
from src.Solver_Programs.MainSolver import EnhancedJSONEncoder


def hidden_route_performance(real_hidden_routes, inferred_hidden_routes, flag = 0):
    """

    :param real_hidden_routes: list of HiddenRoute objects representing the real hidden routes of the drivers
    :param inferred_hidden_routes: list of HiddenRoute objects representing the inferred hidden routes by the algorithm
    :param flag: boolean flag. If 0: use the function route_similarity() to compute distance. if 1: use the route_distance() function to compute the distance
    :return: the average distance between real hidden routes and the inferred routes
    """
    rt_tuples = []
    for real_rt in real_hidden_routes:  # pairing inferred and real for each driver
        for inf_rt in inferred_hidden_routes:
            if real_rt.dr_id == inf_rt.dr_id:
                rt_tuples.append((real_rt, inf_rt))

    distances = []

    if flag == 0:
        for t in rt_tuples:
          distances.append(1 - route_similarity(t[0], t[1]))

    if flag == 1:
        for t in rt_tuples:
          distances.append(route_distance(t[0].route, t[1].route))

    avg_dist = sum(distances) / len(distances)
    return avg_dist


if __name__ == '__main__':
    with open(f"{dev_data_path}cities.json", 'r') as file:
        cities = json.load(file)

    with open(f"{dev_data_path}items.json", 'r') as file:
        items = json.load(file)

    with open(f"{dev_data_path}drivers.json", 'r') as file:
        drivers = json.load(file)

    with open(f"{data_path}standard.json", 'r') as file:
        std_list = json.load(file)

    std_routes = []

    for standard in std_list:
        trip_list = [Trip(tr["from"], tr["to"], tr["merchandise"]) for tr in standard["route"]]
        std_routes.append(StandardRoute(standard["id"], trip_list))

    limit_trip = [min_trips, max_trips]
    limit_items = [min_items, max_items]
    limit_card = [min_card, max_card]

    hidden_routes = generate_hidden_routes([Driver(dr, None) for dr in drivers], cities, items, limit_trip, limit_items, limit_card)

    # genera actual
    actual_routes = []  # list of actuals serialized in json objects (compatibility for hidden_route_finder)
    actuals_per_driver = 0
    n_drivers = len(drivers)
    ID = 0
    std_for_dr = {dr: [] for dr in drivers}  # list of standards implemented by every driver
    inferred_hiddens = []
    perf_for_iter = []
    actuals_for_iter = []


    iterations = 100  # number of execution of the algorithm with incrementing dataset size
    for _ in range(iterations):
        prev = actuals_per_driver
        actuals_per_driver += 10
        for driver in drivers:
            hidden_route = next((hid for hid in hidden_routes if hid.dr_id == driver), None)
            for _ in range(prev, actuals_per_driver):
                random_std = sample(std_routes, 1)[0]  # pick a random std route to implement )object StandardRoute
                std_for_dr[driver].append(random_std)
                act = generate_actual_route(hidden_route = hidden_route, std_route = random_std, list_of_cities=cities, list_of_items=items, ID=ID)  # hidden_route must be an object Hidden, random_std has to be an object StandardRoute. OK
                ID += 1

                actual_routes.append(json.loads(json.dumps(act, cls=EnhancedJSONEncoder)))
                for trip in actual_routes[-1]['route']:
                    trip['from'] = trip.pop('departure')
                    trip['to'] = trip.pop('destination')
                    trip['merchandise'] = trip.pop('merchandise')
            json_std = json.loads(json.dumps(std_for_dr[driver], cls=EnhancedJSONEncoder))
            for route in json_std:
                for trip in route['route']:
                    trip['from'] = trip.pop('departure')
                    trip['to'] = trip.pop('destination')
                    trip['merchandise'] = trip.pop('merchandise')
            jsn_act = [dr_act for dr_act in actual_routes if dr_act["driver"] == driver]

            inf_hid = hidden_route_finder(json_std, jsn_act, driver, DEBUG = True)# need routes in json format
            inferred_hiddens.append(inf_hid)

        avg_perf = hidden_route_performance(hidden_routes, inferred_hiddens, flag = 0)
        #perf_for_iter.append((actuals_per_driver, avg_perf))
        perf_for_iter.append(avg_perf)
        actuals_for_iter.append(actuals_per_driver)

    # plot the performance

    plt.plot(actuals_for_iter, perf_for_iter, label = 'Hidden_route_finder() performance')
    plt.xlabel('number of actual routes implemented by each driver')
    plt.ylabel('avg distance between inferred hidden and real hidden routes')
    plt.legend()
    plt.savefig("dist.png")


