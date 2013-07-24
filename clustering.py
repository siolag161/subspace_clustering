
########## CLASSES #################
def string_to_set(string, sep = ","):
    objects = set([int(elem) for elem in string.split(sep)])
    return objects

def list_to_string(set_of_elements, sep = ","):
    elements = list(set_of_elements)
    return sep.join([str(elem) for elem in elements])
    
class SubspaceCluster:
    """
    a class representing a subspace cluster
    i.e. pair of objects/dimensions
     """
    def __init__(self, clustering_id, objects, dimensions):
        self.clustering_id = clustering_id
        self._process_objects(objects)
        self._process_dimensions(dimensions)
        

    def __str__(self):
        """ TODO: """
        _str = "[objects = %s] - [dimensions = %s]" %(self.objects_str, self.dimensions_str)
        return _str

    def _process_objects(self, objects, sep = ","):        
        typename = objects.__class__.__name__
        if (typename == 'str'):
            self.objects = string_to_set(objects, sep)            
            self.objects_str = objects
        else:
            """ list or set """
            self.objects = set(sorted(objects))
            self.objects_str = list_to_string(self.objects)
            
    
    def _process_dimensions(self, dimensions, sep = ","):
        typename = dimensions.__class__.__name__
        if (typename == 'str'):
            self.dimensions = string_to_set(dimensions, sep)            
            self.dimensions_str = dimensions
        else:
            """ list or set """
            self.dimensions = set(sorted(dimensions))
            self.dimensions_str = list_to_string(self.dimensions)

    
class SubspaceClustering:
    """ a class representing a subspace clustering: list of clusters"""
    def __init__(self, algorithm, parameters, run,
                 clustering_id = None, clusters = [],  
                 contains_noise = False, clustering_on_dimension = False):
        self.algorithm = algorithm
        self.parameters = parameters
        self.run = run
        self.clusters = clusters
        
        self.contains_noise = contains_noise        
        self.clustering_on_dimension = clustering_on_dimension # to determine wherether we distingust clustering by their dimension projection or by run

        if not clustering_id:
            self.clustering_id = self._generate_id()
        else:
            self.clustering_id  = clustering_id


    def set_contains_noise(self, val):
        self.contains_noise = val
            
    def contains_noise(self):
        return self.contains_noise

    def set_clustering_on_dimension(self, val):
        self.clustering_on_dimension = val
        self.clustering_id = self._generate_id()

    def _generate_id(self):
        if self.clustering_on_dimension:
            clustering_id = "%s_(%s)_(%s)_(%s)" %(self.algorithm, self.parameters, str(self.run), self.clusters[0].dimensions_str)
        else:
            clustering_id = "%s_%s_%s" %(self.algorithm,self. parameters, str(self.run))
                
        return clustering_id

    def get_objects(self):
        """ return the union of all objects from all clusters """
        objs = set()
        for cluster in self.clusters:
            objs.update(cluster.objects)

        return objs

    def add_cluster(self, cluster):
        if not cluster.clustering_id and self.clustering_id:
            cluster.clustering_id = self.clustering_id
        
        if self.clustering_id == cluster.clustering_id:
            self.clusters.append(cluster)

    def __key(self):
        return self.generate_id()

    def __eq__(x, y):
        return x.__key() == y.__key()

    def __hash__(self):
        return hash(self.__key())
        
    
class MeasureMixin:
    """ mixins (a particular pythnic syntatic sugar) for measures/values dictionary """
    from collections import defaultdict
    def __init__(self, **measures):
        if measures:
            self.__dict__.update(measures)

    def set_value(self, key, value):
        #self.measures[key] = value
        self.__dict__[key] =val

    def get_value(self, key):
        #return self.measures.get(key)
        return self.__dict__[key]

    def update_measures(self, measures):
        #self.measures.update(measures)
        #return self.__dict__[key]
        self.__dict__.update(measures)
        
    def get_measure_names(self):
        #return self.measures.keys()    
        return self.__dict__.keys()

##################################### import/export from CSV  ####################################
FIELD_NAMES = ["algorithm", "parameters", "run", "dimensions", "objects"]  
    
def write_clustering(clusterings, basic_fields, measure_fields, ofile, with_clusters = True):
    """ write to file the clustering with optional additional measure fields. 
    the with_cluster indicates wherether we write at clustering or cluster level"""
    import csv

    clustering_written_count = 0
    with open(ofile, 'wb') as out_file:
        print("writing data to %s..." %(ofile))

        fields = list(basic_fields)
        fields.extend(measure_fields)
        writer = csv.DictWriter(out_file, delimiter=',', fieldnames=fields)
        writer.writerow(dict((fn,fn) for fn in fields))

        
        for clustering in clusterings:
            #print basic_fields, clustering.__dict__['clustering_id']

            #print clustering.__dict__
            clustering_written_count += 1
            if (clustering_written_count % 200 == 0): print "already written: %d clusterings..." %(clustering_written_count)
            if with_clusters:
                for cluster in clustering.clusters:
                    row_basic = dict((fn, clustering.__dict__[fn]) for fn in basic_fields if  clustering.__dict__.has_key(fn))
                    row_basic.update(dict((fn, cluster.__dict__[fn]) for fn in basic_fields if  cluster.__dict__.has_key(fn)
                                     and not clustering.__dict__.has_key(fn)))
                    row_measure = dict((fn, clustering.__dict__[fn]) for fn in measure_fields if  clustering.__dict__.has_key(fn))
                    
                    row = dict(row_basic)
                    row.update(row_measure)                   
                
                    row.update({'objects': cluster.objects_str, 'dimensions': cluster.dimensions_str})

                    #print row                
                    writer.writerow(row)
            else:
                row_basic = dict((fn, clustering.__dict__[fn]) for fn in basic_fields if  clustering.__dict__.has_key(fn))
                row_measure = dict((fn, clustering.__dict__[fn])  for fn in measure_fields if  clustering.__dict__.has_key(fn))                    
                row = dict(row_basic)
                row.update(row_measure)   
                writer.writerow(row)
            

def read_clusterings(ifile, basic_fields, measure_fields, contains_noise_ = False, clustering_on_dimension_ = False, is_cluster_level=True):
    """ import clustering from a csv-like text file. the field names are used to limit the fields we want to read
    return a list of clusterings. """
    import csv

    clusterings = {}
    with open(ifile, 'rb') as in_file:
        print("reading %s to get data..." %(ifile))
        file_dialect = csv.Sniffer().sniff(in_file.read(1024))
        in_file.seek(0)

        field_names = list(basic_fields); field_names.extend(measure_fields)        
        reader = csv.DictReader(in_file,  dialect = file_dialect)
        
        reader.next() 

        line_count = 0
        for row in reader:
            clustering = SubspaceClustering(algorithm = row['algorithm'], parameters=row['parameters'], run=row['run'],
                 clustering_id = row['clustering_id'], clusters = [],  
                 contains_noise = contains_noise_, clustering_on_dimension =  clustering_on_dimension_)

            clustering_id = row['clustering_id']
            clusterings.setdefault(clustering_id, clustering)
            if is_cluster_level:
                cluster = SubspaceCluster(clustering_id, dimensions = row['dimensions'], objects = row['objects'])
                clusterings[clustering_id].add_cluster(cluster)

            for measure in measure_fields:
                 clusterings[clustering_id].__dict__[measure] = float(row[measure])
            
    return clusterings.values()


###############################################################################################################
def read_matrix_data(ifile):
    """ read from an extended bedgraph-like file to a numpy array"""
    import csv
    import numpy as np
    with open(ifile, 'rb') as in_file:
        print("reading %s to get data..." %(ifile))
        file_dialect = csv.Sniffer().sniff(in_file.read(1024))
        in_file.seek(0)
        
        reader = csv.reader(in_file, dialect = file_dialect)
        reader.next()

        line_count = 0
        for row in reader:
            line_count += 1
            vals = row[3:]
            if (line_count == 1):
                data = np.array(vals, dtype=np.float64)
            else:
                data = np.vstack((data, np.array(vals, dtype=np.float64)))
                
        return data


        
############################### KM-Clustering ########################################
class KMClustering(SubspaceClustering, MeasureMixin):
    """ basically it is a subspace clustering but might contain some additonal information such as a list of measures/values"""
    def __init__(self, algorithm, parameters, run,
                 clustering_id = None, clusters=[], ccontains_noise = False, cclustering_on_dimension = False, **measures):
        
        SubspaceClustering.__init__(self, algorithm = algorithm, parameters = parameters, run = run, clustering_id = clustering_id, clusters=clusters,  contains_noise = ccontains_noise, clustering_on_dimension = cclustering_on_dimension)

        MeasureMixin.__init__(self, **measures)

######################################################################################
""" useful helper functions """
def my_combi(data, dimensions, projection_dimension_size, nbr_step = 50, number_of_clusters = 4, threshold = 1e-5):
    """ at each yield, return a k-combination project from a data of n-dimensions """
    from itertools import combinations
    for projection in combinations(dimensions, projection_dimension_size):
        yield data[:,projection], projection, nbr_step, number_of_clusters, threshold


######################################  K-MEANS ################################################



        
