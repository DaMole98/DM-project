'''
This script extracts the preferences of the drivers
'''
from typing import List

from src.Class_Structures.ClassesDefinition import Route, StandardRoute, ActualRoute, Trip
import numpy as np

from src.Data_Generator.Parameters.parameters import data_path
from src.Solver_Programs.jsonutils import find_sets, reorder_data


def route_to_matrix(route: Route, itemset: List, cityset: List):
    matrix = np.zeros((len(itemset), len(cityset)))
    for t_index, trip in enumerate(route.route):
        city = trip.departure
        column_index = cityset.index(city)
        for merch, card in trip.merchandise.items():
            row_index = itemset.index(merch)
            prev_card = route.route[t_index - 1].merchandise[merch] if (t_index > 0 and (merch in route.route[t_index - 1].merchandise)) else 0
            matrix[row_index, column_index] = card - prev_card

    for merch, card in trip.merchandise.items():
        row_index = itemset.index(merch)
        matrix[row_index, column_index] = 0 - card

    return matrix

#def matrix_to_route(matrix, itemset, cityset): #TODO



if __name__ == "__main__":
    import json

    DEBUG = True

    datapath = "./Output/tmp/routes_implementation.json"
    # loads sets from files and reorder data
    # load standards
    with open(f"{data_path}standard.json", 'r') as file:
        std_list = json.load(file)

    with open(f"{data_path}actual.json", 'r') as file:
        act_list = json.load(file)
        reorder_data(act_list, datapath)
        itemset, cityset = find_sets(act_list)

    # Now, for each driver, creates a list of standard route that she implements
    # and, for each standard route, create a list of actuals that implements the standard.
    with open(datapath, 'r') as file:
        drivers = json.load(file)  # temporaneo: trovare un modo per leggere il file a chunk
        # altrimenti ci tocca tenere tutto in memoria

    driver_preferences = dict()
    if DEBUG: drivers_pref_matrices = dict()
    # These loops  iterate trhough the multi-level hash table represented by the json (dict is an hashtable)
    for driver, standards in drivers.items():  # driver is a key standards is an inner dict
        partial_prefs = []
        for standard, actuals in standards.items():  # standard is the key, actuals is an inner dict

            std_description = next((std for std in std_list if std["id"] == standard), None)
            trip_list = [Trip(tr["from"], tr["to"], tr["merchandise"]) for tr in std_description["route"]]
            std_route = StandardRoute(std_description["id"], trip_list)
            std_matrix = route_to_matrix(std_route, itemset, cityset)
            divergences_from_std = []

            for actual, trips in actuals.items():
                trip_list = [Trip(tr["from"], tr["to"], tr["merchandise"]) for tr in trips]
                act_route = ActualRoute(actual, trip_list, driver, standard)
                act_matrix = route_to_matrix(act_route, itemset, cityset)
                divergences_from_std.append(act_matrix - std_matrix)

            mean_divergence_on_std = sum(divergences_from_std) / len(divergences_from_std)
            partial_pref = std_matrix + mean_divergence_on_std
            partial_prefs.append(partial_pref)

        preference = sum(partial_prefs) / len(partial_prefs)
        #hidden_route = matrix_to_route(preference)
        #driver_preferences[driver] = hidden_route

        if DEBUG:
            drivers_pref_matrices[driver] = preference
            #dumping preference matrixes on json file (for debugging)

    if DEBUG:
        raw_pref_dump = {dr: pr.tolist() for (dr, pr) in drivers_pref_matrices.items()}
        with open("./Output/tmp/prefDump.json", 'w') as file:
            json.dump(raw_pref_dump, file, indent=4)

        #check if the preferences found contains (are similar to) the cities in hte real preferences

        city_prefs = {dr: [] for dr in drivers.keys()}

        for driver in city_prefs.keys():
            for col_ind in range(drivers_pref_matrices[driver].shape[1]):
                if not np.all(drivers_pref_matrices[driver][:, col_ind] == 0):
                    city_prefs[driver].append(cityset[col_ind])
            city_prefs[driver].sort()

        with open("./Output/tmp/guessed_city_prefDump.json", 'w') as file:
            json.dump(city_prefs, file, indent=4)

        real_city_prefs = {dr: [] for dr in drivers.keys()}

        with open(data_path + "HiddenRoutes.json", 'r') as file:
            jsn = json.load(file)
            for rt in jsn:
                for tr in rt["route"]:
                    real_city_prefs[rt["driver_id"]].append(tr["departure"])
                real_city_prefs[rt["driver_id"]].append(tr["destination"])
                real_city_prefs[rt["driver_id"]].sort()

        with open("./Output/tmp/real_city_prefDump.json", 'w') as file:
            json.dump(real_city_prefs, file, indent=4)




        #hidden_route_matrices = {driver: None for driver, None in drivers.keys()}


