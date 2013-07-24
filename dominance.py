from measures import * 

##################### SIMILARITY ########################
def cluster_structural_similarity(cluster1, cluster2):
    """ compute the similarity between cluster1 and cluster2. basically it is a pair of object 
    similarity and dimension similarity. and by similarity we mean precision. """
    
    object_similarity = precision_sets(cluster1.objects, cluster2.objects)
    dimension_similarity = precision_sets(cluster1.dimensions, cluster2.dimensions)

    return (object_similarity, dimension_similarity)

def is_structurally_similar(ref_cluster, target_cluster, object_threshold = 0.5, dimension_threshold = 0.5):
    """ checks whether the ref cluster is simlar to target cluster, w.r.t the two threshold. this relation is
    based on the calculation of precision, thus not being symetric nor transitive. they have belong to the same clustering i.e clustering_ids equal """
    if ref_cluster.clustering_id != target_cluster.clustering_id: return False #clustering_id equality
    object_similarity, dimension_similarity = cluster_structural_similarity(ref_cluster, target_cluster)
    return object_similarity >= object_threshold and dimension_similarity >= dimension_threshold

def is_inferior(ref_cluster, target_cluster, func):
    """ check whether a ref_cluser is inferior to another one w.r.t a evaluator f """
    return func(ref_cluster) < func(target_cluster)

def is_dominated(ref_cluster, target_cluster, func, objs_threshold = 0.5, dims_threshold = 0.5):
    """ check whether a ref_cluser is inferior to another one w.r.t a evaluator f """
    return is_inferior(ref_cluster, target_cluster, func) and  is_structurally_similar(ref_cluster, target_cluster, objs_threshold, dims_threshold)

############################################## DOMINANCE #########################################
def non_dominated_clusters(clusters, func, dim_thres = 0.5, obj_thres = 0.5):
    """ filter out the non_dominated ones from a set of clusters. the processus of non_dominated finding
    is a bit complicated..

    it consists of:
    1. find a set of non_dominated (either dominant or isolated), called A
    2. among dominated: find the those who are not being by any of A, called B
    3. the result is the merge of A&B"""
    
    #clusters = clustering.clusters
    sorted(clusters, key = func, reverse = True)
    sz = len(clusters) # nbr of clusters contained in this clustering

    dominance = {}
    for i in xrange(sz):
        clA = clusters[i]
        for j in xrange(i+1, sz):
            clB = clusters[j]                 
            if is_dominated(clB, clA, func, dim_thres, obj_thres):
                dominance.setdefault(j, set())
                dominance[j].add(i)

    dominated_candidate_idx = dominance.keys(); 
    non_dominated_idx = [i for i in xrange(sz) if i not in dominated_candidate_idx]; 
   
        #print 'dominants: %s' %(non_dominated_idx)
        
    for cand in dominated_candidate_idx:
        selected = True
        for non_dom in non_dominated_idx:
            if is_dominated(clusters[cand], clusters[non_dom], func, dim_thres, obj_thres):
                selected = False                
                break
        if selected:
            non_dominated_idx.append(cand)
            
    non_dominated = [clusters[i] for i in non_dominated_idx]
    return non_dominated_idx, non_dominated

def non_dominated_clustering(clustering, func, dim_thres = 0.5, obj_thres = 0.5):
    """ patch redundancy filtering for a list of clusterings """
    return non_dominated_clusters(clustering.clusters, func, dim_thres, obj_thres)

def non_dominated_clusterings(clusterings, func, dim_thres = 0.5, obj_thres = 0.5, clustering_filter = True):
    """ patch redundancy filtering for a list of clusterings """
    clts = []
    for clustering in clusterings:
        non_dominated_idx, non_dominated = non_dominated_clustering(clustering,func, dim_thres, obj_thres)
        if (len(non_dominated_idx)<2):
            continue
        else:
            clts.append(clustering)
    return clts



######################## SOME EVALUATOR FUNCTIONS ##################################
def cardinality_func(cluster):
    """ a func which compute the interestingness in term of product of cardinality of object times(x) the cardinality of dimensions"""
    return float(len(cluster.objects)*len(cluster.dimensions))

