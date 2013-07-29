
# ccontains_noise = False, cclustering_on_dimension

ALGORITHM_LIST = ['KMEANS', 'SUBCLU', 'SC-KMEANS', 'PROCLUS']

ALGORITHM_NOISE = {'KMEANS':0, 'SUBCLU':0, 'PROCLUS':1, 'SC-KMEANS':0,}
""" whether it contains the noise cluster. by default no  """

ALGORITHM_SHARE_DIMENSION = {'KMEANS':1, 'SUBCLU':0, 'PROCLUS':0, 'SC-KMEANS':0,}
""" whether all the clusters share the same dimension (for instance K-means). by default no  """


class SubspaceAlgorithmLookupError(Exception):
    pass

class SubspaceAlgorithmLookup:
    """TODO: change to a real property look-up """
    def __init__(self):
        pass

    def algorithm_contains_noise_cluster(self, algo_name):
        if ALGORITHM_NOISE.has_key(algo_name):
            return ALGORITHM_NOISE[algo_name]
        else:
            return 0

    def algorithm_shares_dimension(self, algo_name):
        if ALGORITHM_SHARE_DIMENSION.has_key(algo_name):
            return ALGORITHM_SHARE_DIMENSION[algo_name]
        else:
            return 0
    
    def get_property(self, algorithm_name, property_name):
        if property_name == 'contains_noise':
            return self.algorithm_contains_noise_cluster(algorithm_name)

        if property_name == 'shares_dimension':
            return self.algorithm_shares_dimension(algorithm_name)

        else:
            raise SubspaceAlgorithmLookupError("Unknown property...")
