from ClusterManager import ClusterManager
from Config import Config
from Templatize import Templatize

templatize = Templatize(debug=True, objects=['Lead', 'Opportunity', 'Note'], mds_path=Config.mds_path, patterns=['VO.xml.xml'])

for pattern in templatize.patterns:
    cluster = ClusterManager.get_cluster(pattern)
    for artifact in cluster.get_artifacts():
        artifact.print_xml()
        print 'Done..'

for pattern in templatize.patterns:
    cluster = ClusterManager.get_cluster(pattern)
    cluster.get_template().print_xml()