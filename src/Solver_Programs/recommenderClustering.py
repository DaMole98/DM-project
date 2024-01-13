from typing import List
from similarityMeasure import route_similarity
from random import sample
from sklearn.cluster import KMeans


def cluster_routes(std_routes, actual_routes, clusters):
    """
    This function fits the actual routes set into clusters and returns the labels

    :param std_routes: list of StandardRoute object
    :param actual_routes:  list of ActualRoutes object
    :param clusters: number of clusters to generate
    :return: list of tuples that contains the ActualRoute object and the relative cluster label
    """



    dimensions = 10 # dimension of the space in which we cluster data
    #sample template routes
    template_routes = sample(std_routes, dimensions)

    #actual_ids = []
    # compute the hash vector of the routes
    route_hashes = []
    for route in actual_routes:
        #actual_ids.append(route.id)
        route_hashes.append([route_similarity(route, template_routes[i]) for i in range(dimensions)])
    #print(route_hashes)

    kmeans = KMeans(n_clusters = clusters)
    kmeans.fit(route_hashes)
    route_labels = list(zip(actual_routes, kmeans.labels_))
    return route_labels




    


