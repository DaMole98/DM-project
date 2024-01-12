'''
This file contains the parameters of the problem
'''

def get_parameters():
    '''
    returns a dictionary containing the parameters of the problem

    :return: dictionary containing the parameters of the problem
    :param min_trips: minimum number of trips per route
    :param max_trips: maximum number of trips per route
    :param min_items: minimum number of items per trip
    :param max_items: maximum number of items per trip
    :param min_card: minimum cardinality of an item in a trip
    :param max_card: maximum cardinality of an item in a trip
    :param data_path: path to the data folder
    :param dev_data_path: path to the dev_data folder
    '''
    return {
        "min_trips": min_trips,
        "max_trips": max_trips,
        "min_items": min_items,
        "max_items": max_items,
        "min_card": min_card,
        "max_card": max_card,
        "data_path": data_path,
        "dev_data_path": dev_data_path,
        "num_drivers": num_drivers,
        "MAX_STD_ROUTE_PER_DRIVER": MAX_STD_ROUTE_PER_DRIVER,
        "MAX_IMPLEMENTATIONS_PER_DRIVER": MAX_IMPLEMENTATIONS_PER_DRIVER,
        "size_dataset": size_dataset,
    }


act_routes_num = 50 #number of actual routes to be generated
std_routes_num = 100 #number of routes to be generated

min_trips = 10
max_trips = 20 #bounds on the number of trips per route. Ensure that this value does not exceed hte number of cities minus one
               #(otherwise the same city will appear more times in a route. This could make sense in certain cases)
min_items = 10
max_items = 30 #maximum number of types of items per trip

min_card = 10
max_card = 150 #cardinality of a specified item in a trip

MAX_DRIVERS_PER_SROUTE = 5 #maximum number of drivers per route
MAX_IMPLEMENTATIONS_PER_DRIVER = 10 #maximum number of implementations per driver

MAX_STD_ROUTE_PER_DRIVER = 10 #number of standard routes implemented by a driver

num_drivers = 100 # number of drivers to be generated
size_dataset = "medium1" #size of the dataset to be generated. It can be "small", "medium" or "large"

data_path = "../../data/"
dev_data_path = f"{data_path}dev_data/"