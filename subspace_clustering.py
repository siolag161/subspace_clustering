from measures import *
from clustering import *
from dominance import *

############################################### Entry point ##########################################################
FIELD_BASIC = ["algorithm", "parameters", "run", "dimensions", "objects", "clustering_id"]  
#FIELD_MEASURE = ['spatial_coherence', 'distortion']
CLUSTERING_FIELD_BASIC = ["algorithm", "parameters", "run", "clustering_id", ]   

import sys, getopt
from numpy import random
from numpy.random import rand
 
def usage():
    """ in short: we can specify input (containing the information regarding the clusterings provided by the algorithms)
    and the ouput (concerning the scores/ranks). Other options: redundancy filtering or not, output both clusterings/clusters or both,
    include or not the information regarding the ranks of each clustering in the list. TODO: add the parellelism """    

    print '[USAGE]: subspace_clustering.py -i <inputfile> -r <reference-clustering path should be at the cluster_level> -o <outputfile> -c <output: 1 or cluster-level, otherwise it is clustering level> -f <Filtering or not> -t <in case of filtering is enabled, specifies which to output: the original (0), the filtered (1) or both (otherwise)> -d <dimension threshold> -o <object threshold>'

def main(argv):
    """ TODO: look up algorithm in order to know whether it contains noise or not"""
    import time

    
    inputfile = ''
    reffile = ''
    outputfile = ''    
    is_at_cluster_level = True
    #rank_included = False
    redundancy_filtering = False
    filter_choice = 0    
    #on_dim = True
    #noise = False
    dims_thres = 0.5
    objs_thres = 0.5
    
    try:
        opts, args = getopt.getopt(argv,"hi:o:c:f:t:r:",["ifile=", "ofile=", "clust", "redundant",
                                                                  "filter","rfile","noise"])
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
        elif opt in ("-r", "--rfile"):
            reffile = arg
        elif opt in ("-c", "--clust"):
            is_at_cluster_level = (arg=='1')
        elif opt in ("-f", "--redundant"):
            redundancy_filtering = (arg=='1')
        elif opt in ("-f", "--filter"):
            filter_choice = int(arg)
        elif opt in ("-j", "--objt"):
            objs_thres = float(arxg)
        elif opt in ("-d", "--dimt"):
            dims_thres = float(arg)


    begin_time = time.time()
    
    print 'reading %s to generate reference clustering...' %(reffile)
    hidden_clustering = read_clusterings(ifile = reffile, basic_fields =CLUSTERING_FIELD_BASIC,measure_fields=[],
                                          is_cluster_level=True)[0] 

    
    print 'reading %s target clusterings...' %(reffile)
    original_clusterings = read_clusterings(ifile = inputfile, basic_fields=CLUSTERING_FIELD_BASIC,measure_fields=[],
                                 is_cluster_level=is_at_cluster_level)       

    
    func = cardinality_func
    if redundancy_filtering:
        print 'processing the redundancy filtering...'
        filtered_clusterings = non_dominated_clusterings(original_clusterings, func, dim_thres = dims_thres,
                                                         obj_thres = objs_thres, clustering_filter = True)        

    else:
        filtered_clusterings = original_clusterings

    print 'length of filtered_clusterings = %d' %(len(filtered_clusterings))
    measures = {'f1':lambda(x): f1_score_clustering(hidden_clustering, x),
                    'entropy': lambda(x): entropy_score_clustering(hidden_clustering, x),
                'spatial_contiguity': lambda(x): spatial_coherence(x, np.shape(x)[0]),
                    'rnia': lambda(x): rnia_score(hidden_clustering, x),
                    'ce': lambda(x): ce_score(hidden_clustering, x) }
    
    print 'computing rankings & scores for clusterings with ranks...'
    scored_clusterings = rank_measure(original_clusterings, measures)

    print 'writing scored clusterings with ranks...'
    #write_clustering(clusterings, basic_fields, measure_fields, ofile, with_clusters = True)
    write_clustering(clusterings = scored_clusterings, basic_fields = CLUSTERING_FIELD_BASIC,measure_fields=[],
                     ofile=outputfile, with_clusters = True)

    ofname = ".%s_scoring.csv" %(get_file_name(outputfile))
    write_clustering(clusterings = scored_clusterings, basic_fields = CLUSTERING_FIELD_BASIC,measure_fields=measures.keys(),
                     ofile=ofname, with_clusters = False)
    print 'all done. time taken: %s' %(time.time()-begin_time)
        

def get_file_name(file_path):
    #fname = file_path.split('/')[-1]
    fname = file_path.split('.')[-2]
    return fname
    
    
if __name__ == '__main__':
    import time

    t0 = time.time()
    main(sys.argv[1:])
