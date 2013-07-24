from clustering import *
from hungarian import *
####################################################### SPATIAL COHERENCE #######################################################
def cluster_label_change(cluster, max_size):
    l = len(cluster.objects)
    if l == 0: return 0
    cluster = sorted(cluster.objects) #list(cluster)

    nbr = 0
    nxt = cluster[l-1]

    for i in range(l-1):
        cur = cluster[i]
        nxt = cluster[i+1]
        if (cur+1) != nxt: 
            nbr += 1
    if nxt != max_size-1:
        nbr += 1
    return nbr
    
def clustering_label_change(clustering, max_size):
    """ count the number of label changes for each clustering"""
    if not clustering.clusters:
        return 0
    total = sum([cluster_label_change(clt, max_size) for clt in clustering.clusters])    
    return total

def expected_number_of_changes(clustering, max_size):
    """ expected number """
    nbr_of_clusters = len(clustering.clusters)
    if (nbr_of_clusters == 0): 
        return 0
    sum_of_square = 0
    for cluster in clustering.clusters:
        sum_of_square += len(cluster.objects)**2
    return max_size-sum_of_square*1.0/max_size

def spatial_coherence(clustering, cardinality):    
    """ the tricky part about computing this measure lies in the fact that some clustering contains only non-noise clusters.
    meaning that sometime we have to know the cardinality of the whole dataset"""
    from collections import defaultdict

    if clustering.contains_noise:
        """ add the noisy part as an additional cluster """
        all_objects = set(range(cardinality)) # all objects possible from the data space
        other_objects = all_objects.difference(clustering.get_objects())
        other_cluster = SubspaceCluster(clustering_id = clustering.clustering_id, objects = other_objects, dimensions="")
        all_clusters  = clustering.clusters.append(other_cluster)
        
    
    nbr_changes = clustering_label_change(clustering, cardinality)
    expected  = expected_number_of_changes(clustering, cardinality)

    #print "nbr_changes=%s, expected=%s" %(nbr_changes, expected)
    if not expected: return 0.0, 1

    return float(nbr_changes-expected)/(cardinality-expected), 1

####################################################### f1 #######################################################
# 2 helpers for computing the precision and the recall between 2 sets
def set_convert(ls):
    if ls.__class__.__name__ !='set':
        ls = set(ls)
    return ls

def precision_sets(set1, set2):
    """ computes the precision score of 2 sets"""

    set1, set2 = set_convert(set1), set_convert(set2)
    intersection = set1.intersection(set2)
    if set1:
        return float(len(intersection))/len(set1)
    return 0.0

def recall_sets(set1, set2):
    """ computes the recall of 2 sets """
    return precision_sets(set2, set1)

#f1
def f1_score(set1, set2, beta = 1):
    """ if b > 1 that means the completeness is more important (weighted more) than the homogeneity """
    precision = precision_sets(set1, set2)
    recall = recall_sets(set1, set2)

    if (precision+recall == 0): return 0.0

    return (1+beta)*(precision*recall)/(beta*precision+recall)




####################################################### F1-Score #####################################################
def f1_hidden_cluster_map(ref_clustering, target_clustering, beta = 1):
    """ each found cluster is mapped to the hidden cluster 
    which is covered to the most part by this found cluster"""
    mapped_hidden = {}
    hidden_clusters = ref_clustering.clusters

    for clust in target_clustering.clusters:
        
        mapped_precision = -1
        for hclust in hidden_clusters:
            
            precision = precision_sets(hclust.objects, clust.objects)
            if precision > mapped_precision:
                mapped_precision = precision
        if mapped_precision > 0:
            for hclust in hidden_clusters:
                if mapped_precision == precision_sets(hclust.objects, clust.objects):
                    mapped_hidden.setdefault(hclust, set())
                    mapped_hidden[hclust].update(clust.objects)
    return mapped_hidden
                

def f1_score_clustering(ref_clustering, target_clustering, beta = 1):
    if not ref_clustering.clusters or not target_clustering.clusters:
        return 0.0

    nbr_of_hidden = len(ref_clustering.clusters) # number of hidden clusters    
    mapped_clusters = f1_hidden_cluster_map(ref_clustering, target_clustering, beta)
    
    total_f1 = 0.0
    for hidden_cluster, mapped_objects in mapped_clusters.iteritems():
        #print "%s, %s, %s"%(hidden_cluster.objects, mapped_objects,f1_score(hidden_cluster.objects, mapped_objects))
        total_f1 += f1_score(hidden_cluster.objects, mapped_objects)

    return total_f1/float(nbr_of_hidden)

####################################################### Entropy #######################################################
def entropy_score_cluster(ref_clustering, target_cluster):
    import math
    etp = 0.0
    for clust in ref_clustering.clusters: #for each cluster of the hidden clustering
        """ the precision can be seen as the shared fraction/proba"""
        proba = precision_sets(target_cluster.objects, clust.objects) #compute the precision(target, hidden)
        if (proba != 0):
            etp += -proba*math.log(proba)                
    return etp
    
def entropy_score_clustering(ref_clustering, target_clustering):
    import math
    """ compute the entropy-measure of clustering. entropy is a metric to measure the homogeneity of
        a clustering. it should contains mainly objects from one ref cluster. a split is deemed to have bad quality"""
    if not ref_clustering.clusters or not target_clustering.clusters:
        return 0.0
    m = len(ref_clustering.clusters)
    entropy_max = math.log(m)

    entropy_max_sum =  entropy_max*sum([len(p.objects) for p in target_clustering.clusters])
    if (entropy_max_sum == 0):
        return 1.0-0.0
    else:
        entropy_weighted_sum = sum(len(p.objects)*entropy_score_cluster(ref_clustering, p)
                                   for p in target_clustering.clusters)
            
        entropy_weighted_average = float(entropy_weighted_sum)/entropy_max_sum;
        return 1.0-entropy_weighted_average    

#######################################################  RNIA  ######################################################
def rnia_clustering_coordonates(clustering):
    """ return a list of pair depicting the coordonates of the micro-objects """
    rs = set([])
    
    for cluster in clustering.clusters:
        for row in cluster.objects:
            for col in cluster.dimensions:
                rs.add((row, col))
                    
    return rs   
    

def rnia_score(ref_clustering, target_clustering):
     ref_coord = rnia_clustering_coordonates(ref_clustering)
     target_coord = rnia_clustering_coordonates(target_clustering)
     
     union = float(len(set.union(ref_coord, target_coord)))
        
     if union ==0:
         return 0.0
     
     intersection = len(set.intersection(ref_coord, target_coord))    
     
     return 1-(union-intersection)/union


#######################################################  CE  #######################################################

def cluster_intersection(clustA, clustB):
        rsA = set([])
        for row in clustA.objects:
                for col in clustA.dimensions:
                    rsA.add((row, col))

        rsB = set([])
        for row in clustB.objects:
                for col in clustB.dimensions:
                    rsB.add((row, col))

        intersection = rsA.intersection(rsB)

        return len(intersection)


def make_ce_matrix(ref_clustering, target_clustering):
    #clt = clustering    
    ref_clusters = ref_clustering.clusters
    target_clusters = target_clustering.clusters
    
    nbr_row = len(ref_clusters) 
    nbr_col = len(target_clusters)
    mat = 0*np.ones([nbr_row, nbr_col], dtype=int)    
    for i in xrange(nbr_row):
        for j in xrange(nbr_col):
            ref_clust = ref_clusters[i]
            target_clust = target_clusters[j]
            mat[i,j] = cluster_intersection(ref_clust, target_clust)
    return mat
        
def clustering_error(ref_clustering, target_clustering):
    mat = make_ce_matrix(ref_clustering, target_clustering)
    
    ref_coord = rnia_clustering_coordonates(ref_clustering)
    target_coord = rnia_clustering_coordonates(target_clustering)
    U = float(len(set.union(ref_coord, target_coord)))
    
    if U ==0:        
        return 0.0    
    
    hung_solver = Hungarian()
    rs, D_Max = hung_solver.compute(mat, True)    
    
    if U==0:
        return 0        
    return 1-(U-D_Max)/(U)

def ce_score(ref_clustering, target_clustering):
    return clustering_error(ref_clustering, target_clustering)

###########################################################################################################
##########################################  RANKING ########################################################
###########################################################################################################
def rank_measure(clusterings, measures, measures_reverse = None):
    """ returns the order ot clusterings in terms of measures. measurs_revese
    indicate whether we should reverse the order. we require that these two have the same lenghts"""
    import scipy.stats as ss
    import numpy as np
    from collections import defaultdict

    if not measures_reverse:
        measures_reverse = defaultdict(int)
    
    rank_dict = {}              
    score_dict = {}
    for measure in measures.keys():
        measure_func, smaller_is_better = measures[measure], measures_reverse[measure]
        data = []
        for clustering in clusterings:
            clustering.__dict__[measure] = measure_func(clustering)
            if smaller_is_better:            
                data.append(clustering.__dict__[measure])
            else:
                data.append(clustering.__dict__[measure]) # reverse the sign in order to sort better            
        ranking = ss.rankdata(data)
        #print measure, data
        rk_measure = 'rk_%s'% (measure)
        for i in xrange(len(clusterings)):
            clusterings[i].__dict__[rk_measure] = ranking[i]
        
    return clusterings #sorted_dict
    

############################### EVALUATOR ############################
