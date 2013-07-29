from km import *
from clustering import *
from measures import *
from hungarian import *
from dominance import *

from subspace_algorithm import SubspaceAlgorithmLookup

import dominance

import unittest 

class TestSubspaceAlgorithm(unittest.TestCase):
    def test_subspace_algorithm_share_dimension(self):
        cl_a = SubspaceCluster("a", [1,2,3], [1,2,3])
        cl_b = SubspaceCluster("b", [1,2,3], [1,2,3])
        cl_c = SubspaceCluster("b", [1,2,3], [1,2,3])

        lookup = SubspaceAlgorithmLookup()
        algo = 'KMEANS'

        clustering_id = "kmeans_params_1_1,2,3"
        clustering = SubspaceClustering(algorithm = algo,
                                        parameters='parameters', run=1,
                                        clustering_id = clustering_id, clusters = [cl_a, cl_b, cl_c])

        
        self.assertEqual,(lookup.get_property(algo, 'contains_noise'), 0)
        #self.assertFalse(is_structurally_similar(cl_a, cl_b, 0.5, 0.5))
