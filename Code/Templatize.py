import os
from ClusterManager import ClusterManager
from ArtifactManager import ArtifactManager
from Config import Config

"""
mds_path = '/Users/cghai/Documents/Code/BaselineTemplating/ActiveMDS'
objects = ['Opportunity', 'Lead']
Opportunity/oracle/apps/custom/model/mdssys/cust/Site/SITE/ResourceRegistry.rpx.xml
Opportunity/oracle/apps/sales/opptyMgmt/opportunities/opportunityService/mdssys/cust/Site/SITE/Opportunity.xsd.xml
Opportunity/xliffBundles/override/oracle/apps/sales/opptyMgmt/opportunities/resource/OpptyMgmtOpportunitiesAttrBundle.xlf
Opportunity/xliffBundles/override/oracle/apps/sales/opptyMgmt/opportunities/resource/mdssys/cust/Site/SITE/OpptyMgmtOpportunitiesAttrBundle.xlf.xml
Opportunity/xliffBundles/override/oracle/adf/businesseditor/model/util/mdssys/cust/Site/SITE/BaseRuntimeResourceBundle.xlf.xml
Opportunity/xliffBundles/override/oracle/adf/businesseditor/model/util/BaseRuntimeResourceBundle.xlf
Opportunity/persdef/oracle/apps/sales/opptyMgmt/opportunities/model/entity/mdssys/cust/Site/SITE/OpportunityEO.xml.xml
Opportunity/persdef/oracle/apps/sales/opptyMgmt/opportunities/model/entity/OpportunityEO.xml
Opportunity/persdef/oracle/apps/sales/opptyMgmt/opportunities/opportunityService/view/OpportunityVO.xml
Opportunity/persdef/oracle/apps/sales/opptyMgmt/opportunities/opportunityService/view/mdssys/cust/Site/SITE/OpportunityVOOperations.xml.xml
Opportunity/persdef/oracle/apps/sales/opptyMgmt/opportunities/opportunityService/view/mdssys/cust/Site/SITE/OpportunityVO.xml.xml
Opportunity/persdef/oracle/apps/sales/opptyMgmt/opportunities/opportunityService/view/OpportunityVOOperations.xml



Lead/oracle/apps/custom/model/mdssys/cust/Site/SITE/ResourceRegistry.rpx.xml
Lead/oracle/apps/marketing/leadMgmt/leads/leadService/mdssys/cust/Site/SITE/MklLead.xsd.xml
Lead/xliffBundles/override/oracle/apps/marketing/leadMgmt/leads/resource/MklLeadsAttrBundle.xlf
Lead/xliffBundles/override/oracle/apps/marketing/leadMgmt/leads/resource/mdssys/cust/Site/SITE/MklLeadsAttrBundle.xlf.xml
Lead/xliffBundles/override/oracle/adf/businesseditor/model/util/mdssys/cust/Site/SITE/BaseRuntimeResourceBundle.xlf.xml
Lead/xliffBundles/override/oracle/adf/businesseditor/model/util/BaseRuntimeResourceBundle.xlf
Lead/persdef/oracle/apps/marketing/leadMgmt/leads/leadService/view/mdssys/cust/Site/SITE/MklLeadVO.xml.xml
Lead/persdef/oracle/apps/marketing/leadMgmt/leads/leadService/view/mdssys/cust/Site/SITE/MklLeadVOOperations.xml.xml
Lead/persdef/oracle/apps/marketing/leadMgmt/leads/leadService/view/MklLeadVO.xml
Lead/persdef/oracle/apps/marketing/leadMgmt/leads/leadService/view/MklLeadVOOperations.xml
Lead/persdef/oracle/apps/marketing/leadMgmt/leads/model/entity/mdssys/cust/Site/SITE/MklLeadEO.xml.xml
Lead/persdef/oracle/apps/marketing/leadMgmt/leads/model/entity/MklLeadEO.xml
"""
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