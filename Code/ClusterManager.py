from Cluster import Cluster

class ClusterManager:
    pattern_to_cluster = {}

    @staticmethod
    def get_cluster(pattern):
        if pattern not in ClusterManager.pattern_to_cluster:
            ClusterManager.pattern_to_cluster[pattern] = Cluster(pattern)
        return ClusterManager.pattern_to_cluster[pattern]
