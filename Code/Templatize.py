import os
from ClusterManager import ClusterManager
from ArtifactManager import ArtifactManager
from ObjectManager import ObjectManager
from Config import Config
from Util import Util
import copy


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
        self.obj_to_tokens = {}
        self.duplicate_tokens = {}
        self.preprocess()
        self.process()
        self.shrink_tokens()
        self.complete()


    def get_objects(self):
        return self.objects

    def get_patterns(self):
        return self.patterns

    def preprocess(self):
        for obj in self.objects:
            for root, dirs, files in os.walk(os.path.join(self.mds_path, obj)):
                for afile in files:
                    file_path = os.path.join(root, afile)
                    object = ObjectManager.get_obj(obj)
                    for pattern in self.patterns:
                        if file_path.endswith(pattern):
                            cluster = ClusterManager.get_cluster(pattern)
                            artifact = ArtifactManager.get_artifact(file_path)
                            cluster.add_artifact(artifact)
                            artifact.set_cluster(cluster)
                            artifact.set_obj(obj)
                            object.add_artifact(artifact)
                            break

    def process(self):
        for pattern in self.patterns:
            cluster = ClusterManager.get_cluster(pattern)

            print "Processing Cluster " , cluster.get_name()
            cluster.get_processed_template()
            print "Done Cluster " , cluster.get_name()


    def shrink_tokens(self):

        obj_to_all_tokens = {}
        obj_to_value_to_key = {}
        obj_to_unique_tokens = {}
        for cur_obj in self.objects:
            self.obj_to_tokens[cur_obj] = {}
            obj_to_all_tokens[cur_obj] = ObjectManager.get_obj(cur_obj).get_all_tokens()
            obj_to_value_to_key[cur_obj] = {}
            obj_to_unique_tokens[cur_obj] = {}

        ref_obj = self.objects[0]
        all_tokens_ref_obj = obj_to_all_tokens[ref_obj]
        value_to_key_ref_obj = obj_to_value_to_key[ref_obj]

        for token_name,token_value in sorted(all_tokens_ref_obj.items()):
            duplicate = False
            if token_value in value_to_key_ref_obj:
                duplicate = True
                orig_token = value_to_key_ref_obj[token_value]
                for cur_obj in self.objects:
                    value_to_key_cur_obj = obj_to_value_to_key[cur_obj]
                    all_tokens_cur_obj = obj_to_all_tokens[cur_obj]
                    if orig_token != value_to_key_cur_obj[all_tokens_cur_obj[token_name]]:
                        duplicate = False
                        break

            if duplicate:
                for cur_obj in self.objects:
                    self.obj_to_tokens[cur_obj][token_name] = orig_token
                self.duplicate_tokens[token_name] = orig_token
            else:
                for cur_obj in self.objects:
                    all_tokens_cur_obj = obj_to_all_tokens[cur_obj]
                    self.obj_to_tokens[cur_obj][token_name] = all_tokens_cur_obj[token_name]
                    value_to_key_cur_obj = obj_to_value_to_key[cur_obj]
                    value_to_key_cur_obj[all_tokens_cur_obj[token_name]] = token_name
                    obj_to_unique_tokens[cur_obj][token_name] = all_tokens_cur_obj[token_name]


        for cur_obj_name in self.objects:
            cur_obj = ObjectManager.get_obj(cur_obj_name)
            cur_obj.set_unique_tokens(obj_to_unique_tokens[cur_obj_name])

    def complete(self):
        dup_token_rev_map = {}
        for k,v in self.duplicate_tokens.items():
            dup_token_rev_map[v] = k
        for pattern in self.patterns:
            cluster = ClusterManager.get_cluster(pattern)
            final_cluster_template = copy.deepcopy(cluster.get_artifacts()[0].get_template())
            Util.tokenize(final_cluster_template.getroot(), self.duplicate_tokens)
            self.cluster_to_template[cluster.get_name()] = final_cluster_template
            cluster.set_final_template(final_cluster_template)


    def get_template(self, cluster_name):
        return self.cluster_to_template[cluster_name]