from ClusterManager import ClusterManager
from Config import Config
from Templatize import Templatize
import sys
import os
import shutil
import xml.etree.ElementTree as ET

templatize = Templatize(debug=True, objects=sys.argv[1].split(','), mds_path=Config.mds_path, patterns=sys.argv[2].split(','))
out_dir = sys.argv[3]

for pattern in templatize.patterns:
    os.chdir(out_dir)
    cluster = ClusterManager.get_cluster(pattern)
    cluster.get_template()
    dir_name = cluster.get_name().replace('.','_')
    shutil.rmtree(dir_name, ignore_errors=True)
    os.mkdir(dir_name)
    os.chdir(out_dir + "/" + dir_name)
    artifacts = cluster.get_artifacts()
    template = artifacts[0].get_template()
    template.write('SmartBaseline.xml')
    for artifact in cluster.get_artifacts():
        tokens = artifact.get_unique_tokens()
        file_name = artifact.get_obj() + '.properties'
        f = open(file_name, 'w')
        for token in sorted(tokens.keys()):
            f.write(token)
            f.write("=")
            f.write(tokens[token])
            f.write("\n")
        f.close()

