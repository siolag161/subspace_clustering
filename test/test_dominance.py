from km import *
from clustering import *
from measures import *
from hungarian import *
from dominance import *
import dominance

import unittest 

class TestDominance(unittest.TestCase):
    def test_is_similar_different_clustering(self):
        cl_a = SubspaceCluster("a", [1,2,3], [1,2,3])
        cl_b = SubspaceCluster("b", [1,2,3], [1,2,3])
        self.assertFalse(is_structurally_similar(cl_a, cl_b, 0.5, 0.5))
        
    def test_is_similar_exact1(self):
        cl_a = SubspaceCluster("a", [1,2,3], [1,2,3])
        cl_b = SubspaceCluster("a", [1,2,3], [1,2,3])
        self.assertTrue(is_structurally_similar(cl_a, cl_b, 0.5, 0.5))

    def test_is_similar_exact2(self):
        cl_a = SubspaceCluster("a", [1,2,3], [1,2,3])
        cl_b = SubspaceCluster("a", [1,2,3], [1,2,3])
        self.assertTrue(is_structurally_similar(cl_a, cl_b, 1, 1))

    def test_is_similar_different1(self):
        cl_a = SubspaceCluster("a", [1,2,3], [1,2,3])
        cl_b = SubspaceCluster("a", [2,3,4], [2,3,4,5])
        self.assertTrue(is_structurally_similar(cl_a, cl_b, 0.5, 0.5))

    def test_is_similar_different2(self):
        cl_a = SubspaceCluster("a", [1,2,3], [1,2,3])
        cl_b = SubspaceCluster("a", [2,3,4], [2,3,4,5])
        self.assertFalse(is_structurally_similar(cl_a, cl_b, 0.7, 0.5))

    def test_similarity_1(self):
        cl_a = SubspaceCluster("a", [1,2,3], [1,2,3])
        cl_b = SubspaceCluster("a", [2,3,4], [2,3,4,5])
        self.assertEqual(cluster_structural_similarity(cl_a, cl_b), (2.0/3, 2.0/3))

    def test_similarity_2(self):
        cl_a = SubspaceCluster("a", [1,2,3], [1,2,3])
        cl_b = SubspaceCluster("a", [2,3,4], [2,3,4,5])
        self.assertEqual(cluster_structural_similarity(cl_b, cl_a), (2.0/3, 0.5))

    def test_is_inferior(self):
        cl_a = SubspaceCluster("a", [1,2,3], [1,2,3])
        cl_b = SubspaceCluster("a", [2,3,4,6], [2,3,4,5])
        self.assertTrue(is_inferior(cl_a, cl_b, func = dominance.cardinality_func))

    def test_is_dominated(self):
        cl_a = SubspaceCluster("a", [1,2,3], [1,2,3])
        cl_b = SubspaceCluster("a", [2,3,4,6], [2,3,4,5])
        self.assertTrue(is_structurally_similar(cl_a, cl_b, 0.5, 0.5))
        self.assertTrue(is_dominated(cl_a, cl_b, func = dominance.cardinality_func, objs_threshold = 0.5, dims_threshold = 0.5))


    def test_similarity_filter(self):
        """ 2 < 1, 3<1; 5 isolated; 3 < 4, 3 < 2; """
        cluster_1 = SubspaceCluster("a", [1,2,3,4], [1,2,3,4])
        cluster_2 = SubspaceCluster("a", [3,4,8], [3,4,8,12])
        cluster_3 = SubspaceCluster("a", [2,3,8], [3,4,8])
        cluster_4 = SubspaceCluster("a", [2,3,7,9], [3,4,7,10])
        cluster_5 = SubspaceCluster("a", [7,8,10], [7,8,11])

        clusters = [cluster_1, cluster_2, cluster_3, cluster_4, cluster_5]        
        non_dominated_idx, _ = non_dominated_clusters(clusters, func = dominance.cardinality_func, dim_thres = 0.5, obj_thres = 0.5)
        self.assertEqual(non_dominated_idx, [0, 3, 4])

    def test_dominance_case1(self):        
        """ 2 < 1, 1<4; 5 isolated;  3 < 2; -> (1,3,5) """
        cluster_1 = SubspaceCluster("a", [1,2,3,4], [1,2,3,4])
        cluster_2 = SubspaceCluster("a", [3,4,8], [3,4,8,12])
        cluster_3 = SubspaceCluster("a", [4,8], [4,8,12])
        cluster_4 = SubspaceCluster("a", [2,3,7], [3,4,7])
        cluster_5 = SubspaceCluster("a", [7,8,10], [7,8,11])

        clusters = [cluster_1, cluster_2, cluster_3, cluster_4, cluster_5]
        for i in xrange(len(clusters)):
            for j in xrange(i+1,len(clusters)):
                if is_dominated(clusters[i], clusters[j], func = dominance.cardinality_func, objs_threshold = 0.5, dims_threshold = 0.5):
                    print "%d<%d" %(i+1,j+1)
                if is_dominated(clusters[j], clusters[i], func = dominance.cardinality_func, objs_threshold = 0.5, dims_threshold = 0.5):
                    print "%d<%d" %(j+1,i+1)
        clusters = [cluster_1, cluster_2, cluster_3, cluster_4, cluster_5] 
                   
        non_dominated_idx, _ = non_dominated_clusters(clusters, func = dominance.cardinality_func, dim_thres = 0.5, obj_thres = 0.5)
        
        self.assertEqual(sorted(non_dominated_idx), [0, 2, 4])
        
    def test_dominance_case2(self):
        """3<1;4<1;3<2;4<2;5<3;5<4; -> (1,3,5) """
        cluster_1 = SubspaceCluster("a", [3,4,5,6], [1,2,3,4])
        cluster_2 = SubspaceCluster("a", [3,4,5,6], [3,4,5,6])
        cluster_3 = SubspaceCluster("a", [3,4,8], [3,4,8])
        cluster_4 = SubspaceCluster("a", [4,5,9], [3,4,9])
        cluster_5 = SubspaceCluster("a", [4,8,9], [3,4])

        clusters = [cluster_1, cluster_2, cluster_3, cluster_4, cluster_5]
        for i in xrange(len(clusters)):
            for j in xrange(i+1,len(clusters)):
                if is_dominated(clusters[i], clusters[j], func = dominance.cardinality_func, objs_threshold = 0.5, dims_threshold = 0.5):
                    print "%d<%d" %(i+1,j+1)
                if is_dominated(clusters[j], clusters[i], func = dominance.cardinality_func, objs_threshold = 0.5, dims_threshold = 0.5):
                    print "%d<%d" %(j+1,i+1)
        clusters = [cluster_1, cluster_2, cluster_3, cluster_4, cluster_5]                    
        non_dominated_idx, _ = non_dominated_clusters(clusters, func = dominance.cardinality_func, dim_thres = 0.5, obj_thres = 0.5)        
        self.assertEqual(sorted(non_dominated_idx), [0, 1, 4])

    def test_dominance_case3(self):
        pass
