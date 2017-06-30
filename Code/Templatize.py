import os
from ClusterManager import ClusterManager
from ArtifactManager import ArtifactManager
from Config import Config


class Templatize:

    def __init__(self, debug, mds_path = None, objects = None, patterns = None):
        self.debug = True
        if debug:
            self.patterns = patterns
            self.mds_path = mds_path
            self.objects = objects
        else:
            self.patterns = Config.patterns
            self.mds_path = Config.mds_path
            self.objects = Config.objects

        self.obj_to_files = {}
        self.cluster_to_template = {}
        self.preprocess()
        self.process()

    def get_objects(self):
        return self.objects

    def get_patterns(self):
        return self.patterns

    def preprocess(self):
        for obj in self.objects:
            self.obj_to_files[obj] = []
            for root, dirs, files in os.walk(os.path.join(self.mds_path, obj)):
                for afile in files:
                    file_path = os.path.join(root, afile)
                    self.obj_to_files[obj].append(file_path)
                    for pattern in self.patterns:
                        if file_path.endswith(pattern):
                            cluster = ClusterManager.get_cluster(pattern)
                            artifact = ArtifactManager.get_artifact(file_path)
                            cluster.add_artifact(artifact)
                            artifact.set_cluster(cluster)
                            artifact.set_obj(obj)
                            break

    def process(self):
        for pattern in self.patterns:
            cluster = ClusterManager.get_cluster(pattern)

            print "Processing Cluster " , cluster.get_name()
            cluster.get_template()
            print "Done Cluster " , cluster.get_name()




