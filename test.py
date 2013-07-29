from clustering import *
from measures import *
from numpy import random
from numpy.random import rand
from pareto import *


"""" useful helper functions """
def clusters_from_code(code, nbr_of_cluster, dims):
    import numpy as np
    clusters = []    
    dims = set(dims)
    for label in xrange(nbr_of_cluster):
        objs = set(np.where(code == label)[0])
        #print np.where(code == label)
        cluster = SubspaceCluster(clustering_id = None, objects = objs, dimensions = dims)
        clusters.append(cluster) 
    
    return clusters
    
def my_combi(data, dimensions, projection_dimension_size, nbr_step = 50, number_of_clusters = 4, threshold = 1e-5):
    """ at each yield, return a k-combination project from a data of n-dimensions """
    from itertools import combinations
    for projection in combinations(dimensions, projection_dimension_size):
        yield data[:,projection], projection, nbr_step, number_of_clusters, threshold

def kmeans(features, projection, ite = 20, k = 4, threshold = 1e-4):    
    """ perform k_keamns clustering and return a the result as a subsapce clustering object """
    from scipy.cluster.vq import kmeans, vq
    import datetime

    from measures import spatial_coherence    
   
    centroids, distance = kmeans(features, k, iter=ite, thresh=threshold)
    #code, _ = vq(features, centroids)
    
    run_ = datetime.datetime.now().strftime("%y_%m_%d_%H_%M")
    
    params = "projection_size=%d, k=%d" %(len(projection), k)
    #clusters = clusters_from_code(code, k, projection)
  
    clustering_id = "(%s)_(%s)_(%s)_(%s)" %("exhaustive_kmeans", params, run_, projection)
    #print clustering_id
    km_clt = KMClustering(algorithm ="exhaustive_kmeans", parameters = params, run = run_,
      clustering_id = clustering_id, clusters = [], ccontains_noise = False, cclustering_on_dimension = True)

   
    #measures = {'spatial_coherence': spatial_coherence(km_clt, len(features))[0], 'distortion': distance}
    #km_clt.update_measures(measures)
    
    return  km_clt 
        

def kmeans_args(params):
    data, projection, ite, k, threshold = params   
    return kmeans(data, projection, ite, k, threshold)

def kmeans_execute(data, dimensions_size, number_of_clusters = 4, processes = 7):    
    import multiprocessing
    """ the data here is an numpy multi-array"""
    
    pool = multiprocessing.Pool(processes)

    dimensions = np.shape(data)[1]    
    features = my_combi(data, xrange(dimensions), dimensions_size)      
    rs = pool.map(kmeans_args, features)    
    pool.close()
    pool.join()
    
    return rs

        

################################################################## 
def main():
    
    import time
    from scipy.cluster.vq import whiten
    #random.seed((1030,2000))

    print 'generating data...'
    data = np.random.rand(2700, 15)

    
    t = time.time()

    print 'executing km_just...'
    km = kmeans_execute(data, dimensions_size = 4, number_of_clusters = 4, processes = 7)
    print (len(km))
    print 'writing km_just...'
    write_clustering(km, basic_fields = FIELD_BASIC, measure_fields = FIELD_MEASURE,  ofile = "./test_km_ouput_just.csv", with_clusters = True)
   
    
    t1 = time.time()-t
    print 'taken %s' %(t1)

    """
    print 'executing km_nm...'
    km = kmeans_execute(data, dimensions_size = 4, number_of_clusters = 4, processes = 7, is_just = False)
    print 'writing km_nm...'
    write_clustering(km, basic_fields = FIELD_BASIC, measure_fields = FIELD_MEASURE,  ofile = "./test_km_ouput._nm.csv", with_clusters = True)
   
    print (len(km))
    t2 = time.time()-t1
    print 'taken %s' %(t2)
    """    

if __name__ == "__main__":   
    import time
    from scipy.cluster.vq import kmeans, vq
    
    #main()
    data = np.random.rand(2700, 4)
    t1 = time.time()
    for i in xrange(1000):
        centroids,_ = kmeans(data, 4, 10, 1e-1)
    t2 = time.time()-t1
    print 'taken %s' %(t2)

   
    
