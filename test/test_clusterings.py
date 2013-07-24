from km import *
from clustering import *
from measures import *

import unittest 

class TestKmClustering(unittest.TestCase):
    def test_kmclustering_construction(self):
        kmc = KMClustering(algorithm = "sexton", parameters = "k=4", run = 1, clustering_id = None, spatial_coherence = 1, distortion = 2)
        self.assertEqual(kmc.algorithm, "sexton")
        self.assertEqual(kmc.parameters, "k=4")
        self.assertEqual(kmc.run, 1)
        self.assertEqual(kmc.get_value("spatial_coherence"), 1)
        self.assertEqual(kmc.get_value("distortion"), 2)

    def test_cluster_construction(self):        
        cluster1 = SubspaceCluster(clustering_id = "", objects = [1,2,3], dimensions = [3,5,1])
        self.assertEqual(cluster1.objects_str, "1,2,3")
        self.assertEqual(cluster1.dimensions_str, "1,3,5")

        cluster2 = SubspaceCluster(clustering_id = "", objects = "1,2,3", dimensions = "3,2,1")
        self.assertEqual(cluster2.objects_str, "1,2,3")
        self.assertEqual(cluster2.dimensions_str, "3,2,1") # not sorted - not a bug, acutally expected

        

    def test_clustering_construction(self):
        cluster1 = SubspaceCluster(clustering_id = "test1", objects = [0, 1,2,3], dimensions = [3,5,1])
        cluster2 = SubspaceCluster(clustering_id = "test1", objects = "4,5,6,7", dimensions = "3,2,1")
        cluster3 = SubspaceCluster(clustering_id = "test1", objects = "8,9", dimensions = "3,2,1")
        cluster4 = SubspaceCluster(clustering_id = "test1", objects = "7", dimensions = "3,2,1")

        clt = SubspaceClustering(algorithm = "algo", parameters = "params", run = 1,
                 clustering_id = "test1", clusters = [cluster1, cluster2, cluster3, cluster4])
        self.assertEqual(clt.clustering_id, "test1")

        clt = SubspaceClustering(algorithm = "algo", parameters = "params", run = 1,
                 clustering_id = None, clusters = [cluster1, cluster2, cluster3, cluster4])
        self.assertEqual(clt.clustering_id, "algo_params_1")

        clt = SubspaceClustering(algorithm = "algo", parameters = "params", run = 1,
                 clustering_id = None, clusters = [cluster1, cluster2, cluster3, cluster4])
        clt.set_clustering_on_dimension(True)
        self.assertEqual(clt.clustering_id, "algo_(params)_(1)_(1,3,5)")
        

    def test_spatial_coherence(self):
        cluster1 = SubspaceCluster(clustering_id = "test1", objects = [0, 1,2,3], dimensions = [3,5,1])
        cluster2 = SubspaceCluster(clustering_id = "test1", objects = "4,5,6", dimensions = "3,2,1")
        cluster3 = SubspaceCluster(clustering_id = "test1", objects = "8,9", dimensions = "3,2,1")
        cluster4 = SubspaceCluster(clustering_id = "test1", objects = "7", dimensions = "3,2,1")

        clt = SubspaceClustering(algorithm = "algo", parameters = "params", run = 1,
                 clustering_id = "test1", clusters = [cluster1, cluster2, cluster3, cluster4])
        self.assertEqual(spatial_coherence(clt, 10)[0], -4.0/3)


        cluster1 = SubspaceCluster(clustering_id = "test1", objects = "7,1,3,9", dimensions = [3,5,1])
        cluster2 = SubspaceCluster(clustering_id = "test1", objects = "8", dimensions = "3,2,1")
        cluster3 = SubspaceCluster(clustering_id = "test1", objects = "4", dimensions = "3,2,1")
        cluster4 = SubspaceCluster(clustering_id = "test1", objects = "0,2,5,6", dimensions = "3,2,1")

        clt = SubspaceClustering(algorithm = "algo", parameters = "params", run = 1,
                 clustering_id = "test1", clusters = [cluster1, cluster2, cluster3, cluster4])
        self.assertEqual(spatial_coherence(clt, 10)[0], (8-6.6)/(10-6.6))
