from km import *
from clustering import *
from measures import *
from hungarian import *
import unittest 

class TestMeasures(unittest.TestCase):
    def test_precision(self):
        clust_a = SubspaceCluster("clustering_id", [1,2,3,4,5], [1,2,3])
        clust_b = SubspaceCluster("clustering_id", [3,4,5,7], [2,3,5,6,7])
        precision_objs_ab = precision_sets(clust_a.objects, clust_b.objects)
        precision_dims_ab = precision_sets(clust_a.dimensions, clust_b.dimensions)
        self.assertEqual(precision_objs_ab, 3.0/5)
        self.assertEqual(precision_dims_ab, 2.0/3)

        clust_a = SubspaceCluster("clustering_id", [], [1,2,3])
        clust_b = SubspaceCluster("clustering_id", [3,4,5,7], [])
        precision_objs_ab = precision_sets(clust_a.objects, clust_b.objects)
        precision_dims_ab = precision_sets(clust_a.dimensions, clust_b.dimensions)
        self.assertEqual(precision_objs_ab, 0.0/5)
        self.assertEqual(precision_dims_ab, 0.0/3)

        clust_a = SubspaceCluster("clustering_id", [1,2,3,4], [1,2,3])
        clust_b = SubspaceCluster("clustering_id", [1,2,3,4], [1,2,3])
        
        self.assertEqual(precision_sets(clust_a.objects, clust_b.objects), 1)
        self.assertEqual(precision_sets(clust_a.dimensions, clust_b.dimensions), 1)

    def test_recall(self):        
        clust_a = SubspaceCluster("clustering_id", [1,2,3,4,5], [1,2,3])
        clust_b = SubspaceCluster("clustering_id", [3,4,5,7], [2,3,5,6,7])
        precision_objs_ba = precision_sets(clust_b.objects, clust_a.objects)
        precision_dims_ba = precision_sets(clust_b.dimensions, clust_a.dimensions)

        recall_objs_ab = recall_sets(clust_a.objects, clust_b.objects)
        recall_dims_ab = recall_sets(clust_a.dimensions, clust_b.dimensions)
        self.assertEqual(precision_objs_ba, recall_objs_ab)
        self.assertEqual(precision_dims_ba, recall_dims_ab)

    def test_f1_cluster(self):
        clust_a = SubspaceCluster("clustering_id", [1,2,3,4,5,6], [1,2,3])
        clust_b = SubspaceCluster("clustering_id", [2,3,4,7], [2,3,5,6,7])
        f1_ab = f1_score(clust_a.objects, clust_b.objects)
        f1_ba = f1_score(clust_b.objects, clust_a.objects)
        self.assertEqual(f1_ab, f1_ba)
        self.assertEqual(f1_ab, 0.6)

    def test_f1_clustering(self):
        hidden_clust_1 = SubspaceCluster("hidden_clustering_id", [1,2,5,6], [1,2,3])
        hidden_clust_2 = SubspaceCluster("hidden_clustering_id", [3,7,8], [2,3,5,6,7])
        hidden_clust_3 = SubspaceCluster("hidden_clustering_id", [1,3,5,7], [2,3,5,6,7])
        hidden_clust_4 = SubspaceCluster("hidden_clustering_id", [2,4,5,7,8], [2,3,5,6,7])
        hidden_clustering = SubspaceClustering(algorithm="hidden_clustering", parameters="", run=1,
                 clustering_id = "hidden_clustering_id", clusters = [hidden_clust_1, hidden_clust_2,
                 hidden_clust_3, hidden_clust_4], contains_noise = False, clustering_on_dimension = False)

        
        found_clust_11 = SubspaceCluster("found_clustering_id1", [1,2,3,4,5,6], [1,2,3])
        found_clust_12 = SubspaceCluster("found_clustering_id1", [2,3,5,7], [2,3,5,6,7])
        found_clust_13 = SubspaceCluster("found_clustering_id1", [4,6,7,8], [2,3,5,6,7])
        found_clustering_1 = SubspaceClustering(algorithm="kmeans", parameters="", run=1,
                 clustering_id = "found_clustering_1", clusters = [found_clust_11, found_clust_12,
                 found_clust_13], contains_noise = False, clustering_on_dimension = False)

        mapped = f1_hidden_cluster_map(hidden_clustering, found_clustering_1)

        true_val = 0.25*(0.75+0.8+4.0/7+0.0)
        diff = (f1_score_clustering(hidden_clustering, found_clustering_1)-true_val)
        self.assertTrue(round(diff, 5) == 0.0)


        found_clust_21 = SubspaceCluster("found_clustering_id2", [1,2,3,4,5,6], [1,2,3])
        found_clust_22 = SubspaceCluster("found_clustering_id2", [3,4,7], [2,3,5,6,7])
        found_clust_23 = SubspaceCluster("found_clustering_id2", [3,5,6], [2,3,5,6,7])
        found_clust_24 = SubspaceCluster("found_clustering_id2", [2,3,5,6,8], [2,3,5,6,7])
        found_clust_25 = SubspaceCluster("found_clustering_id2", [2,4,5,6,7], [2,3,5,6,7])

        found_clustering_2 = SubspaceClustering(algorithm="found_clustering_2", parameters="", run=2,
                 clustering_id = "found_clustering_2", clusters = [found_clust_21, found_clust_22,
                 found_clust_23, found_clust_24, found_clust_25], contains_noise = False, clustering_on_dimension = False)
        #self.assertEqual(f1_score_clustering(hidden_clustering, found_clustering_2), 0.5)

    def test_entropy(self):
        hidden_clust_1 = SubspaceCluster("hidden_clustering_id", [1,2,5,6], [1,2,3])
        hidden_clust_2 = SubspaceCluster("hidden_clustering_id", [3,7,8], [2,3,5,6,7])
        hidden_clustering = SubspaceClustering(algorithm="hidden_clustering", parameters="", run=1,
                 clustering_id = "hidden_clustering_id", clusters = [hidden_clust_1, hidden_clust_2],
                                               contains_noise = False, clustering_on_dimension = False)
        
        found_clust_11 = SubspaceCluster("found_clustering_id1", [1,2,5,6], [1,2,3])
        found_clust_12 = SubspaceCluster("found_clustering_id1", [3,7,8], [2,3,5,6,7])
        found_clust_13 = SubspaceCluster("found_clustering_id1", [3,7], [2,3,5,6,7])
        found_clust_14 = SubspaceCluster("found_clustering_id1", [1,2,5,6], [2,3,5,6,7])

        found_clustering_1 = SubspaceClustering(algorithm="kmeans", parameters="", run=1,
                 clustering_id = "found_clustering_1", clusters = [found_clust_11, found_clust_12,
                 found_clust_13, found_clust_14], contains_noise = False, clustering_on_dimension = False)

        true_val = 1
        diff = (entropy_score_clustering(hidden_clustering, found_clustering_1)-true_val)
        #self.assertTrue(round(diff, 5) == 0.0)
        self.assertEqual(entropy_score_clustering(hidden_clustering, found_clustering_1), 1.0) #perfect scenario
        
        hidden_clust_1 = SubspaceCluster("hidden_clustering_id", [1], [1,2,3])
        hidden_clust_2 = SubspaceCluster("hidden_clustering_id", [2], [2,3,5,6,7])
        hidden_clustering = SubspaceClustering(algorithm="hidden_clustering", parameters="", run=1,
                 clustering_id = "hidden_clustering_id", clusters = [hidden_clust_1, hidden_clust_2],
                                               contains_noise = False, clustering_on_dimension = False)
        
        found_clust_11 = SubspaceCluster("found_clustering_id1", [1,2], [1,2,3])
        found_clust_12 = SubspaceCluster("found_clustering_id1", [1,2], [2,3,5,6,7])

        found_clustering_1 = SubspaceClustering(algorithm="kmeans", parameters="", run=1,
                 clustering_id = "found_clustering_1", clusters = [found_clust_11, found_clust_12 ],
                                                contains_noise = False, clustering_on_dimension = False)

        true_val = 1
        diff = (entropy_score_clustering(hidden_clustering, found_clustering_1)-true_val)
        #self.assertTrue(round(diff, 5) == 0.0)
        self.assertEqual(entropy_score_clustering(hidden_clustering, found_clustering_1), 0.0) #worst scenario

    def test_rnia(self):
        cl_a1 = SubspaceCluster("", [1,2,3,4],[3,4])
        cl_a2 = SubspaceCluster("", [6,7],[4,5])
        cl_a3 = SubspaceCluster("", [4,5,6],[7,8,9])

        cl_b1 = SubspaceCluster("", [1,2],[3,4])
        cl_b2 = SubspaceCluster("", [3,4],[3,4])
        cl_b3 = SubspaceCluster("", [6,7],[5,6,7,8])

        ref_clustering = SubspaceClustering(algorithm="sckmeans1", parameters="", run=1,
                 clustering_id = "found_clustering_1", clusters = [cl_a1, cl_a2, cl_a3],)
        target_clustering = SubspaceClustering(algorithm="sckmeans2", parameters="", run=2,
                 clustering_id = "found_clustering_2", clusters = [cl_b1, cl_b2, cl_b3],)

        #eva = SubspaceEvaluator(cl_a)
        self.assertEqual(rnia_score(ref_clustering, target_clustering), 12./25)

    def test_hungarian(self):
        import numpy as np
        hg = Hungarian()
        a = np.array([[0, 1], [2, 3], [4, 5]])
        b = np.array([[0, 1, 0], [2, 3, 0], [4,5, 0]])
        self.assertTrue((hg._pad_to_square(a)== b).all())

        matrix = [[1, 2, 3],
              [2, 4, 6],
              [3, 6, 9]]

        hg._init_matrix(matrix)

        #self.assertTrue(hg.compute(matrix),0)
        self.assertEqual(hg._step_1()[1], 2)
        self.assertEqual(hg._step_2()[1], 3)
        self.assertEqual(hg._step_3()[1], 4)
        self.assertEqual(hg._step_4()[1], 6)
        self.assertEqual(hg._step_6()[1], 4)
        self.assertEqual(hg._step_4()[1], 5)
        self.assertEqual(hg._step_5()[1], 3)
        self.assertEqual(hg._step_3()[1], 4)      
        self.assertEqual(hg._step_4()[1], 6)       
        self.assertEqual(hg._step_6()[1], 4)    
        self.assertEqual(hg._step_4()[1], 6)    
        self.assertEqual(hg._step_6()[1], 4)    
        self.assertEqual(hg._step_4()[1], 5)
        self.assertEqual(hg._step_5()[1], 3)     
        self.assertEqual(hg._step_3()[1], 7)  
        

    def test_cost_matrix(self):
        hg = Hungarian()

        c1 = [1, 1, 2, 3, 3, 4, 4, 4, 2]
        c2 = [2, 2, 3, 1, 1, 4, 4, 4, 3]

        mt = hg.make_cost_matrix(c1,c2)
        rs = hg.compute(mt)
        self.assertNotEqual(rs, None)

        
    def test_ce(self):
        cl_a1 = SubspaceCluster("", [1,2,3,4],[3,4])
        cl_a2 = SubspaceCluster("", [6,7],[4,5])
        cl_a3 = SubspaceCluster("", [4,5,6],[7,8,9])

        cl_b1 = SubspaceCluster("", [1,2],[3,4])
        cl_b2 = SubspaceCluster("", [3,4],[3,4])
        cl_b3 = SubspaceCluster("", [6,7],[5,6,7,8])

        ref_clustering = SubspaceClustering(algorithm="sckmeans1", parameters="", run=1,
                 clustering_id = "found_clustering_1", clusters = [cl_a1, cl_a2, cl_a3],)
        target_clustering = SubspaceClustering(algorithm="sckmeans2", parameters="", run=2,
                 clustering_id = "found_clustering_2", clusters = [cl_b1, cl_b2, cl_b3],)

        #eva = SubspaceEvaluator(cl_a)
        self.assertEqual(ce_score(ref_clustering, target_clustering), 1-19./25) 

    
