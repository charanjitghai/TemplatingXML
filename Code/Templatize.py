import os
from ClusterManager import ClusterManager
from ArtifactManager import ArtifactManager
from Config import Config


class Templatize:


    def __init__(self, debug, mds_path = None, objects = None, patterns = None):

        self.debug = True

        self.patterns = patterns
        if patterns is None:
            self.patterns = Config.patterns

        self.mds_path = mds_path
        self.objects = objects if debug else os.listdir(mds_path)
        self.obj_to_files = {}
        self.preprocess()

    def preprocess(self):

        for obj in self.objects:
            self.obj_to_files[obj] = []
            for root, dirs, files in os.walk(os.path.join(self.mds_path, obj)):
                for afile in files:
                    file_name = os.path.join(root, afile).replace(self.mds_path, "")[1:]
                    self.obj_to_files[obj].append(file_name)
                    for pattern in self.patterns:
                        if file_name.endswith(pattern):
                            cluster = ClusterManager.getCluster(pattern)
                            cluster.add_artifact(ArtifactManager.getArtifact(file_name))
                            break






templatize = Templatize(debug=True, objects = Config.objects , mds_path = Config.mds_path)

for pattern in templatize.patterns:
    cluster = ClusterManager.getCluster(pattern)
    for artifact in cluster.get_artifacts():
        artifact.sort()
        print 'Done..'
        #print artifact

"""
debug = True
preprocess(obj_to_files, pattern_to_cluster)
for pattern in patterns:
    cluster = pattern_to_cluster[pattern]
    print pattern, len(cluster.get_files())
# print "\t", pattern_to_cluster[pattern].getFiles()
"""