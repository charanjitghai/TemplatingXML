from ClusterManager import ClusterManager
from Config import Config
from Templatize import Templatize
import sys
import os
import shutil
import xml.etree.ElementTree as ET

"""
cd Opportunity/ 
object.properties
"""
#Opportunity,Lead /Users/cghai/Documents/Code/BaselineTemplating/ActiveMDS VO.xml.xml,EO.xml.xml
templatize = Templatize(debug=True, objects=sys.argv[1].split(','), mds_path=sys.argv[2], patterns=sys.argv[3].split(','))
root_dir = os.getcwd()
for pattern in templatize.patterns:
    os.chdir(root_dir)
    cluster = ClusterManager.get_cluster(pattern)
    cluster.get_template()
    pattern_dir = cluster.get_name().replace('.','_')
    artifacts = cluster.get_artifacts()
    template = artifacts[0].get_template()
    template.write('SmartBaseline.xml')
    for artifact in cluster.get_artifacts():
        tokens = artifact.get_unique_tokens()
        obj_dir = root_dir + '/' + artifact.get_obj()
        os.chdir(obj_dir)
        file_name = 'object.properties'
        f = open(file_name, 'a')
        for token in sorted(tokens.keys()):
            f.write(token)
            f.write("=")
            f.write(tokens[token])
            f.write("\n")
        f.close()

