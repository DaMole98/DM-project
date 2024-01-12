'''
file containing the function that generates the actual routes
'''
from random import random
import src.Class_Structures.ClassesDefinition as cd

def get_probability_parameters():
    """
    Returns a dictionary containing the probability parameters of the problem.

    :return: dictionary containing the probability parameters of the problem
    :param lambda_0: probability of choosing the departure city from the standard route
    :param lambda_1: probability of choosing the departure city from the hidden route
    :param theta_0: probability of choosing the destination city from the standard route
    :param theta_1: probability of choosing the destination city from the hidden route
    :param mu_0: probability of choosing the departure city from the hidden route
    :param mu_1: probability of choosing the departure city from the hidden route
    :param epsilon: neighborhood parameter
    """
    return {
        "lambda_0": lambda_0,
        "lambda_1": lambda_1,
        "theta_0": theta_0,
        "theta_1": theta_1,
        "mu_00": mu_00,
        "mu_01": mu_01,
        "epsilon": epsilon
    }
DEBUG = True

# definition of some constants parameters

# parameters for the actual route generation in the first loop, index std == index hidden route

# parameter for the probability of choosing to change the cities
lambda_0 = 0.5

# parameter for the probability of choosing the city from the hidden route if the previous condition is true
lambda_1 = 0.95


# parameters for the actual route generation in the items loop

# parameter for the probability of choosing to add noise to the items cardinality in the standard route before adding it to the actual route
theta_0 = 0.5

# parameter for choosing an item from the hidden route and adding it to the actual route with a cardinality in the neighborhood of the hidden route item cardinality
theta_2 = 0.5

# parameter for choosing an item from the list of items missing in the actual route and adding it to the actual route
theta_1 = 0.01


# parameters for the actual route generation in the second loop, index std > index hidden route or index std < index hidden route

# parameter for the probability of choosing to add a trip in hidden route to the actual route, if the hidden route is longer than the standard route
mu_00 = 0.5

# parameter for the probability of choosing to change the cities in the hidden route
mu_01 = 0.75


mu_1 = 0.95

# neighborhood parameter
epsilon = 0.05

# definition of the function that generates the actual routes
def generate_actual_route(hidden_route, std_route, list_of_cities, list_of_items, ID):
    """
    Generate an actual route by combining information from a hidden route and a standard route.

    :param hidden_route: A hidden route containing information about the expected route.
    :type hidden_route: Route object

    :param std_route: A standard route representing the baseline for the actual route.


        **Algorithm Overview:**

    1. **Initialization:**
        - Initialize the lengths of the hidden and standard routes.\n

    2. **ActualRoute Creation:**
        - Create an `ActualRoute` object with the given ID and related IDs.\n

    3. **Trip Modification Loop:**
        - Iterate through each trip in the standard route up to the minimum of the hidden and standard route lengths:\n
            a. **Departure City Determination:**
                - Determine the new departure city based on random conditions.\n
            b. **Destination City Determination:**
                - Determine the new destination city based on random conditions.\n
            c. **Merchandise Modification:**
                - Modify the merchandise of the trip based on random conditions and the difference between hidden and standard route cardinalities.\n
            d. **New Trip Creation:**
                - Create a new trip with the determined parameters and append it to the actual route.\n

    4. **Handling Unequal Route Lengths:**
        - Handle cases where the hidden route is longer or shorter than the standard route:\n
            a. **Hidden Route Longer:**
                - If the hidden route is longer, create additional trips with modified parameters.\n
            b. **Standard Route Longer:**
                - If the standard route is longer, create additional trips with modified parameters based on hidden route items.\n

    The algorithm incorporates randomness (coin tosses) and adjustable parameters (lambda_0, lambda_1, theta_0, theta_1, mu_0, epsilon)\n
    to introduce variability in the generated actual route while considering information from both hidden and standard routes.\n
    """
    len_hr = len(hidden_route.route)
    len_sr = len(std_route.route)

    # catch exception if the hidden route is empty or the standard route is empty
    if len_hr == 0 or len_sr == 0:
        return None


    actualRoute = cd.ActualRoute(ID, hidden_route.driver,  std_route.id,[])

    # for each trip in the standard route till the minimum between the length of the hidden route and the length of the standard route
    for i in range(min (len_hr, len_sr)):
        if i == 0:
            new_departure = std_route.route[i].departure
            # toss a coin in range [0,1] and check if it is less than lambda_0
            if random() < lambda_0:
                # toss a coin in range [0,1] and check if it is less than lambda_1
                if random() < lambda_1:
                    # if yes, then the departure city is the same as the one in the hidden route
                    new_departure = hidden_route.route[i].departure
                else:
                    # if no, then the departure city is a random city in the list of cities
                    new_departure = list_of_cities[int(random() * len(list_of_cities))]
        else:
            # the departure city is the same as the destination city of the previous trip
            new_departure = actualRoute.route[i-1].destination

        new_destination = std_route.route[i].destination
        # toss a coin in range [0,1] and check if it is less than theta_0
        if random() < lambda_0:
            # toss a coin in range [0,1] and check if it is less than theta_1
            if random() < lambda_1:
                # if yes, then the destination city is the same as the one in the hidden route
                new_destination = hidden_route.route[i].destination
            else:
                # if no, then the destination city is a random city in the list of cities
                new_destination = list_of_cities[int(random() * len(list_of_cities))]

        # modify the merchandise of the trip
        new_merchandise = []

        for item in std_route.route[i].merchandise:
            # make the difference between the cardinality of the item in the hidden route and the one in the standard route
            # if the item is not in the hidden route, then the cardinality is 0
            new_item_qty = std_route.route[i].merchandise[item]

            # toss a coin in range [0,1] and check if it is less than theta_0
            if random() < theta_0:
                diff = std_route.route[i].merchandise[item]
                if item in hidden_route.route[i].merchandise:
                    diff -= hidden_route.route[i].merchandise[item]

                # limit the neighborhood to epsilon * diff
                neighborhood_limit = random() * 2 * epsilon * diff
                # take a random number in range [ diff - neighborhood_limit, diff + neighborhood_limit ]
                act_diff = int(diff - neighborhood_limit + random() * 2 * neighborhood_limit)
                new_item_qty = new_item_qty - act_diff

            new_item_qty = max(0, new_item_qty)

            if new_item_qty > 0:
                new_merchandise.append((item, new_item_qty))

        for item in hidden_route.route[i].merchandise:
            if item not in std_route.route[i].merchandise:
                # toss a coin in range [0,1] and check if it is less than theta_0
                if random() < theta_2:
                    item_size = hidden_route.route[i].merchandise[item]

                    neighborhood_limit = random() * 2 * epsilon * item_size
                    # take a random number in range [ item_size - neighborhood_limit, item_size + neighborhood_limit ]
                    act_item_size = int(item_size - neighborhood_limit + random() * 2 * neighborhood_limit)
                    act_item_size = max(0, act_item_size)
                    if act_item_size > 0:
                        new_merchandise.append((item, act_item_size))

        for item in list_of_items:
            if item not in std_route.route[i].merchandise and item not in hidden_route.route[i].merchandise:
                # toss a coin in range [0,1] and check if it is less than theta_0
                if random() < theta_1:
                    size = int(random() * random() * random() * 50)
                    if size > 0:
                        new_merchandise.append((item, size))

        # create the new trip
        new_trip = cd.Trip(new_departure, new_destination, dict(new_merchandise))

        # append the new trip to the actual route
        actualRoute.route.append(new_trip)

    if len_hr > len_sr:
        """
        if the hidden route is longer than the standard route, toss a coin in range [0,1] and check if it is less than mu_00 to add a trip
        the trip is modified with noise
        the trip is appended to the actual route
        """
        index = len_sr - 1
        for i in range(len_sr - 1, len_hr - len_sr):
            # print (i, len_sr)
            # if the hidden route is longer than the standard route, toss a coin in range [0,1] and check if it is less than mu_00 to add a trip
            if random() < mu_00:
                if i == 0:
                    new_departure = hidden_route.route[i].departure
                    # toss a coin in range [0,1] and check if it is less than mu_0
                    if random() < mu_01:
                        new_departure = list_of_cities[int(random() * len(list_of_cities))]
                else:
                    # the departure city is the same as the destination city of the previous trip
                    try:
                        new_departure = actualRoute.route[len(actualRoute.route) - 1].destination
                    except IndexError:
                        print("Index error")
                        print(actualRoute.route)
                        print(hidden_route.route)
                        print(std_route.route)
                        print("i = ", i)
                        print("len_sr = ", len_sr)
                        print("len_hr = ", len_hr)
                        print("len(actualRoute.route) = ", len(actualRoute.route))
                        exit(1)

                new_destination = hidden_route.route[i].destination
                # toss a coin in range [0,1] and check if it is less than mu_0
                if random() < mu_01:
                    new_destination = list_of_cities[int(random() * len(list_of_cities))]

                index += 1
                # take all the items in the hidden route and modify their cardinality in neighborhood of the hidden route items cardinality

                new_merchandise = []
                for item in hidden_route.route[i].merchandise:
                    new_item = hidden_route.route[i].merchandise[item]
                    neighborhood_limit = random() * 2 * (epsilon+10) * new_item
                    # take a random number in range [ new_item - neighborhood_limit, new_item + neighborhood_limit ]
                    act_new_item = int(new_item - neighborhood_limit + random() * 2 * neighborhood_limit)
                    act_new_item = max(0, act_new_item)
                    if new_item > 0:
                        new_merchandise.append((item, act_new_item))

                for item in list_of_items:
                    if item not in hidden_route.route[i].merchandise:
                        # toss a coin in range [0,1] and check if it is less than mu_1
                        if random() < theta_1:
                            size = int(random() * random() * random() * 50)
                            if size > 0:
                                new_merchandise.append((item, size))

                # create the new trip
                new_trip = cd.Trip(new_departure, new_destination, dict(new_merchandise))

                # append the new trip to the actual route
                actualRoute.route.append(new_trip)

    elif len_hr < len_sr:
        """
        if the hidden route is shorter than the standard route, toss a coin in range [0,1] and check if it is less than mu_00 to add a trip
        the trip is modified with noise
        the trip is appended to the actual route
        """
        index = len_hr - 1
        for i in range(len_hr - 1 , len_sr - len_hr):
            if random() < mu_00:
                index = i % len_hr
                if i == 0:
                    new_departure = std_route.route[i].departure
                    # toss a coin in range [0,1] and check if it is less than lambda_0
                    if random() < lambda_0:
                        # toss a coin in range [0,1] and check if it is less than lambda_1
                        if random() < lambda_1:
                            # if yes, then the departure city is the same as the one in the hidden route
                            # take i module len_hr to avoid index out of range
                            new_departure = hidden_route.route[index].departure
                        else:
                            # if no, then the departure city is a random city in the list of cities
                            new_departure = list_of_cities[int(random() * len(list_of_cities))]
                else:
                    # the departure city is the same as the destination city of the previous trip
                    new_departure = actualRoute.route[len(actualRoute.route) - 1].destination

                new_destination = std_route.route[i].destination
                # toss a coin in range [0,1] and check if it is less than lambda_0
                if random() < lambda_0:
                    # toss a coin in range [0,1] and check if it is less than lambda_1
                    if random() < lambda_1:
                        # if yes, then the destination city is the same as the one in the hidden route
                        # take i module len_hr to avoid index out of range

                        new_destination = hidden_route.route[index].destination
                    else:
                        # if no, then the destination city is a random city in the list of cities
                        new_destination = list_of_cities[int(random() * len(list_of_cities))]

                # modify the merchandise of the trip
                new_merchandise = []

                for item in std_route.route[i].merchandise:
                    # make the difference between the cardinality of the item in the hidden route and the one in the standard route
                    # if the item is not in the hidden route, then the cardinality is 0
                    new_item = std_route.route[i].merchandise[item]

                    # toss a coin in range [0,1] and check if it is less than lambda_0
                    if random() < lambda_0:
                        diff = std_route.route[i].merchandise[item]
                        if item in hidden_route.route[index].merchandise:
                            diff -= hidden_route.route[index].merchandise[item]

                        neighborhood_limit = random() * 2 * epsilon * diff
                        # take a random number in range [ diff - neighborhood_limit, diff + neighborhood_limit ]
                        act_diff = int(diff - neighborhood_limit + random() * 2 * neighborhood_limit)
                        new_item = new_item - act_diff

                    new_item = max(0, new_item)

                    if new_item > 0:
                        new_merchandise.append((item, new_item))

                for item in hidden_route.route[index].merchandise:
                    if item not in std_route.route[i].merchandise:
                        # toss a coin in range [0,1] and check if it is less than lambda_0
                        if random() < lambda_0:
                            item_size = hidden_route.route[index].merchandise[item]
                            neighborhood_limit = random() * 2 * epsilon * item_size
                            # take a random number in range [ item_size - neighborhood_limit, item_size + neighborhood_limit ]
                            act_item_size = int(item_size - neighborhood_limit + random() * 2 * neighborhood_limit)
                            act_item_size = max(0, act_item_size)
                            if act_item_size > 0:
                                new_merchandise.append((item, act_item_size))

                for item in list_of_items:
                    if item not in std_route.route[i].merchandise and item not in hidden_route.route[index].merchandise:
                        # toss a coin in range [0,1] and check if it is less than lambda_1
                        if random() < theta_1:
                            size = int(random() * random() * random() * 50)
                            if size > 0:
                                new_merchandise.append((item, size))

                # create the new trip
                new_trip = cd.Trip(new_departure, new_destination, dict(new_merchandise))

                # append the new trip to the actual route
                actualRoute.route.append(new_trip)


    return actualRoute