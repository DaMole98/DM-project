from src.Class_Structures.ClassesDefinition import Route
from math import sqrt
def route_similarity(route1 : Route, route2 : Route):

    city1 = set()
    city2 = set()
    items1 = dict()
    items2 = dict()

    #extract merchandise and cities from trips of the two routes
    trip = None
    for trip in route1.route:
        items1[trip.destination] = trip.merchandise
        city1.add(trip.departure)
    city1.add(trip.destination)

    for trip in route2.route:
        items2[trip.destination] = trip.merchandise
        city2.add(trip.departure)
    city2.add(trip.departure)

    city_union = city1.union(city2)
    city_intersection = city1.intersection(city2)
    weighted_intersect = 1 if (route1.route[0].departure == route2.route[0].departure) else 0 #this is the numerator of the weighted jaccard similarity
                                                                                              # 1 if the 2 trips are the same, 0 if they are completely dissimilar
                                                                                              # in (0,1) if the trips are similar (in the cosine sense in the space of items)

    for city in city_intersection: #calculate weight of the city in the intersection (numerator of jaccard similarity)
        it1 = items1[city]
        it2 = items2[city]
        common_it = set(it1.keys()).intersection(set(it2.keys()))
        part_sum = part_1 = part_2 = 0
        for item in common_it:
            part_sum += it1[item] * it2[item]
            part_1 += it1[item]**2
            part_2 += it2[item]**2
        cosine_sim = ( (part_sum / (sqrt(part_1) * sqrt(part_2))) + 1 ) / 2  #calculate cosine similarity and normalize to range [0,1]
        weighted_intersect += cosine_sim

    route_sim = weighted_intersect / len(city_union)
    return route_sim










