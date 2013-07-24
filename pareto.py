import numpy as np
from clustering import *
def pareto_frontier(clusterings, measures, reverse = []):
    """ get a list of clusterings based on the measure indexes passed in the arguments """
    clusterings.sort(key = lambda(x): x.__dict__[measures[0]], reverse = False)
    print "filtering pareto of %d clusterings" %(len(clusterings))
    pareto_frontier = [clusterings[0]]
    for clustering in clusterings[1:]:        
        if sum(clustering.__dict__[measure] >= pareto_frontier[-1].__dict__[measure] for measure in measures) != len(measures):
            pareto_frontier.append(clustering)  
    return pareto_frontier

########################################################## ENTRY ######################################################################
import sys, getopt
from numpy import random
from numpy.random import rand

def usage():
     print '[USAGE]: pareto.py -i <inputfile> -o <outputfile> -c <is at cluster level: 1 for true 0 for clustering level>'

FIELD_BASIC = ["algorithm", "parameters", "run", "clustering_id", "dimensions", "objects"]  
FIELD_MEASURE = ['spatial_coherence', 'distortion']
CLUSTERING_FIELD_BASIC = ["algorithm", "parameters", "run", "clustering_id"]  

def main(argv):
    from scipy.cluster.vq import kmeans, vq, whiten
    inputfile = ''
    outputfile = ''
    dsize = 4
    nclust = 4
    proc = 1
    is_at_cluster_level = True
        
    try:
        opts, args = getopt.getopt(argv,"hi:o:c:",["ifile=","ofile=","cluster"])
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
        elif opt in ("-c", "--cluster"):
            c = int(arg)
            is_at_cluster_level = (c==1)

   
    print 'done reading...'    

    
    print 'done executing kmeans...'
    if is_at_cluster_level:
        SELECTED_FIELD_BASIC, SELECTED_FIELD_MEASURE = FIELD_BASIC, FIELD_MEASURE
    else:
        SELECTED_FIELD_BASIC, SELECTED_FIELD_MEASURE = CLUSTERING_FIELD_BASIC, FIELD_MEASURE
    clusterings = read_clusterings(ifile = inputfile, basic_fields=SELECTED_FIELD_BASIC, measure_fields=SELECTED_FIELD_MEASURE,
                                contains_noise_ = False, clustering_on_dimension_ = False, is_cluster_level=is_at_cluster_level)
    print 'size = %d' %(len(clusterings))
    
    filtered_clusterings = pareto_frontier(clusterings, measures= FIELD_MEASURE, reverse = [])

    write_clustering(filtered_clusterings, basic_fields = SELECTED_FIELD_BASIC, measure_fields = SELECTED_FIELD_MEASURE, ofile = outputfile, with_clusters = is_at_cluster_level)    
    
if __name__ == "__main__":
    import time

    t0 = time.time()
    main(sys.argv[1:])
    print time.time() - t0, "(seconds) elapsed"
