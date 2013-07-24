from km import *
from clustering import *
from measures import *
from hungarian import *
import unittest 

class TestRanking(unittest.TestCase):
    def test_ranking(self):
        hidden_clust_1 = SubspaceCluster("hidden_clustering_id", [1,2,5,6], [1,2,3])
        hidden_clust_2 = SubspaceCluster("hidden_clustering_id", [3,7,8], [2,3,5,6,7])
        hidden_clust_3 = SubspaceCluster("hidden_clustering_id", [1,3,5,7], [2,3,5,6,7])
        hidden_clust_4 = SubspaceCluster("hidden_clustering_id", [2,4,5,7,8], [2,3,5,6,7])
        hidden_clustering = SubspaceClustering(algorithm="hidden_clustering", parameters="", run=1,
                 clustering_id = "hidden_clustering_id", clusters = [hidden_clust_1, hidden_clust_2,
                 hidden_clust_3, hidden_clust_4], contains_noise = False, clustering_on_dimension = False)

        
        found_clust_11 = SubspaceCluster("found_clustering_id1", [1,2,3,4,5,6], [1,2,3])
        found_clust_12 = SubspaceCluster("found_clustering_id1", [2,3,5,7], [2,3,5,6,7])
        found_clust_13 = SubspaceCluster("found_clustering_id1", [4,6,7,8], [2,4,9,6,7])
        found_clustering_1 = SubspaceClustering(algorithm="kmeans_1", parameters="", run=1,
                 clustering_id = "found_clustering_1", clusters = [found_clust_11, found_clust_12,
                 found_clust_13], contains_noise = False, clustering_on_dimension = False)


        found_clust_21 = SubspaceCluster("found_clustering_id1", [1,2,3,4,5,6], [1,2,3])
        found_clust_22 = SubspaceCluster("found_clustering_id1", [2,3,5,7], [2,3,5,6,7])
        found_clust_23 = SubspaceCluster("found_clustering_id1", [4,6,7,8], [1,2,3,7])
        found_clust_24 = SubspaceCluster("found_clustering_id1", [1,3,7,8], [2,3,6,7])
        found_clustering_2 = SubspaceClustering(algorithm="kmeans_2", parameters="", run=1,
                 clustering_id = "found_clustering_2", clusters = [found_clust_21, found_clust_22,
                 found_clust_23, found_clust_24], contains_noise = False, clustering_on_dimension = False)

        found_clust_31 = SubspaceCluster("found_clustering_id1", [1,3,5,6], [1,2,3,4])
        found_clust_32 = SubspaceCluster("found_clustering_id1", [1,2,5,7], [2,6,7,9])
        found_clust_33 = SubspaceCluster("found_clustering_id1", [4,6,7,8], [1,2,7])
        found_clust_34 = SubspaceCluster("found_clustering_id1", [1,3,7,8], [2,6,7])
        found_clust_35 = SubspaceCluster("found_clustering_id1", [1,2,4,8], [1,2,3,6,7])

        found_clustering_3 = SubspaceClustering(algorithm="kmeans_2", parameters="", run=1,
                 clustering_id = "found_clustering_3", clusters = [found_clust_31, found_clust_32,
                 found_clust_33, found_clust_34,  found_clust_35], contains_noise = False, clustering_on_dimension = False)

        #mapped = f1_hidden_cluster_map(hidden_clustering, found_clustering_1)

        measures = {'f1':lambda(x): f1_score_clustering(hidden_clustering, x),
                    'entropy': lambda(x): entropy_score_clustering(hidden_clustering, x),
                    'rnia': lambda(x): rnia_score(hidden_clustering, x),
                    'ce': lambda(x): ce_score(hidden_clustering, x) }

        
        clusterings = [found_clustering_1, found_clustering_2, found_clustering_3]
        ranks = rank_measure(clusterings, measures)
        #for clustering in ranks:
            #print clustering.clustering_id, clustering.__dict__['rk_entropy'], clustering.__dict__['rk_rnia'] , clustering.__dict__['rk_ce'], clustering.__dict__['rk_f1'] 
        #self.assertEqual(ranks, 1)

        
