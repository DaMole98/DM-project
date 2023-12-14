from src.Class_Structures.ClassesDefinition import *
from src.Data_Generator.Parameters.parameters import *


def find_sets(route_list, dump=True):
    itemset = set()
    cityset = set()

    for route in route_list:
        for trip in route['route']:
            cityset.add(trip['from'])
            for item in trip['merchandise'].keys():
                itemset.add(item)
        cityset.add(trip['to'])

    itemset = sorted(itemset)
    cityset = sorted(cityset)

    # Dumping extracted sets on json files (we dont really need them in memory during
    # the execution of the algorithm). We retrieve the data later.
    if dump == True:
        with open("./Output/tmp/itemset.json", 'w') as file:
            dmp = {"num": len(itemset), "items": itemset}
            json.dump(dmp, file, indent=2)
        with open("./Output/tmp/cityset.json", 'w') as file:
            dmp = {"num": len(cityset), "cities": cityset}
            json.dump(dmp, file, indent=2)

    return itemset, cityset


'''
this function reorders the actual.json creating temporary json file which is an array objects, each of which is a driver
with the associated standard routes that he has to follow , and for each standard route there is a list of
actual routes that implements that standard.
This intermediary json is for simplicity of the management of the data and for sorting the
actual on the base of the drivers.The structure is the following:
'''


def reorder_data(act_list, out_filepath):
    drivers = dict()

    for act in act_list:
        dr = act['driver']
        std = act['sroute']
        id = act['id']
        trips = act['route']
        if dr not in drivers:
            drivers[dr] = dict()
        if std not in drivers[dr]:
            drivers[dr][std] = {id: trips}
        else:
            drivers[dr][std][id] = trips

    with open(out_filepath, 'w') as file:
        json.dump(drivers, file, indent=2, sort_keys=True)

# print(drivers)
