from clustering import *
import numpy as np
import multiprocessing
######################################################################################
""" useful helper functions """
def my_combi(data, dimensions, projection_dimension_size, nbr_step = 50, number_of_clusters = 4, threshold = 1e-5):
    """ at each yield, return a k-combination project from a data of n-dimensions """
    from itertools import combinations
    for projection in combinations(dimensions, projection_dimension_size):
        yield data[:,projection], projection, nbr_step, number_of_clusters, threshold
        
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
        
def kmeans(features, projection, ite = 50, k = 4, threshold = 1e-5):    
    """ perform k_keamns clustering and return a the result as a subsapce clustering object """
    from scipy.cluster.vq import kmeans, vq
    import datetime

    from measures import spatial_coherence    
   
    centroids, distance = kmeans(features, k, iter=ite, thresh=threshold)
    code, _ = vq(features, centroids)
    
    run_ = datetime.datetime.now().strftime("%y_%m_%d_%H_%M")
    
    params = "projection_size=%d, k=%d" %(len(projection), k)
    clusters = clusters_from_code(code, k, projection)
  
    clustering_id = "(%s)_(%s)_(%s)_(%s)" %("exhaustive_kmeans", params, run_, projection)
    #print clustering_id
    km_clt = KMClustering(algorithm ="exhaustive_kmeans", parameters = params, run = run_,
                          clustering_id = clustering_id, clusters = clusters, ccontains_noise = False, cclustering_on_dimension = True)

   
    measures = {'spatial_coherence': spatial_coherence(km_clt, len(features))[0], 'distortion': distance}
    km_clt.update_measures(measures)
    
    return  km_clt 

def kmeans_args(params):
    data, projection, ite, k, threshold = params
    return kmeans(data, projection, ite, k, threshold)

def kmeans_execute(data, dimensions_size, number_of_clusters = 4, processes = 7):    
    
    """ the data here is an numpy multi-array"""
    
    pool = multiprocessing.Pool(processes)

    dimensions = np.shape(data)[1]
    
    features = my_combi(data, xrange(dimensions), dimensions_size)      
    rs = pool.map(kmeans_args, features)  
    pool.close()
    pool.join()
    print 'done kmeans. size = %d...' %(len(rs))
    return rs

       
FIELD_BASIC = ["algorithm", "parameters", "run", "dimensions", "objects", "clustering_id"]  
FIELD_MEASURE = ['spatial_coherence', 'distortion']


CLUSTERING_FIELD_BASIC = ["algorithm", "parameters", "run", "clustering_id", ]   

############################################### Entry point ##########################################################
import sys, getopt
from numpy import random
from numpy.random import rand
 
def usage():
     print '[USAGE]: km.py -i <inputfile> -o <outputfile> -d <size of dimension projection> -n <number of clusters> -p <number of parallel processes> -c <is at cluster level: 1 for true 0 for clustering leve>'


def main(argv):
    from scipy.cluster.vq import kmeans, vq, whiten
    inputfile = ''
    outputfile = ''
    dsize = 4
    nclust = 4
    proc = 1
    is_at_cluster_level = True
        
    try:
        opts, args = getopt.getopt(argv,"hi:o:d:n:p:c:",["ifile=","ofile=","dsize","nclust","proc","cluster"])
    except getopt.GetoptError:    
        usage()    
        sys.exit(2)
                
    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-d", "--dize"):
            dsize = int(arg)
        elif opt in ("-n", "--nclust"):
            nclust = int(arg)
        elif opt in ("-p", "--proc"):
            proc = int(arg)
        elif opt in ("-c", "--cluster"):
            c = int(arg)
            is_at_cluster_level = (c==1)
    print 'done reading...'

    data =  read_matrix_data(inputfile)
    data = whiten(data)
    import time
    from scipy.cluster.vq import whiten
    random.seed((1030,2000))

    #whiten datasomewhere
    #print inputfile, outputfile, dsize, nclust,  proc, is_at_cluster_level
    print 'executing kmeans...'
    km = kmeans_execute(data, dimensions_size = dsize, number_of_clusters = nclust, processes = proc)
    print 'done executing kmeans...'
    if is_at_cluster_level:
        SELECTED_FIELD_BASIC, SELECTED_FIELD_MEASURE = FIELD_BASIC, FIELD_MEASURE
    else:
        SELECTED_FIELD_BASIC, SELECTED_FIELD_MEASURE = CLUSTERING_FIELD_BASIC, FIELD_MEASURE
    write_clustering(km, basic_fields = SELECTED_FIELD_BASIC, measure_fields = SELECTED_FIELD_MEASURE, ofile = outputfile, with_clusters = is_at_cluster_level)
    
if __name__ == "__main__":
    import time

    t0 = time.time()
    main(sys.argv[1:])
    print time.time() - t0, "(seconds) elapsed"
