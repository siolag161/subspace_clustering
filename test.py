from clustering import *
from km import *
from measures import *
from numpy import random
from numpy.random import rand
from pareto import *
################################################################## 
def main():
    import sys

    path = sys.argv[1]
    
    print path
    #data =  read_matrix_data(path)
    import time
    from scipy.cluster.vq import whiten
    random.seed((1030,2000))

    data = np.random.rand(120, 8)

    km = kmeans_execute(data, dimensions_size = 4, number_of_clusters = 4, processes = 7)
    #write_clustering(km, basic_fields = FIELD_BASIC, measure_fields = FIELD_MEASURE,  ofile = "./test/test_km_ouput.csv", with_clusters = True)
    # print km
    #clt = km[0]   

    print (len(km))
    clts = pareto_filter(km, ['spatial_coherence', 'distortion'])
    #print clts
    print (len(clts))
        
    #print spatial_coherence(clt, 10) 
    #print(len(clt.clusters))

    

if __name__ == "__main__":   

    main()
    
   
    
