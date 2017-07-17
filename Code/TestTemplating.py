import unittest
from Templatize import Templatize
from Config import Config
from ClusterManager import ClusterManager
from ArtifactManager import Artifact
from Util import Util
import copy


class TestTemplating(unittest.TestCase):

    pattern = 'VO.xml.xml'
    #templatize = Templatize(debug=True, objects=['Opportunity', 'Lead', 'Note', 'Contact', 'Deal', 'BudgetFundRequest', 'SalesObjective', 'TerritoryResource', 'ActivityAssignee',
    #                                             'BusinessPlan', 'DealProduct', 'OpportunityRevenuePartner', 'Reference', 'ServiceRequest'], mds_path=Config.mds_path, patterns=Config.patterns)

    templatize = Templatize(debug=True, objects=['Opportunity', 'Lead', 'Note', 'Contact', 'Deal', 'BudgetFundRequest',
                                                 'SalesObjective', 'TerritoryResource', 'ActivityAssignee', 'DealProduct', 'OpportunityRevenuePartner', 'Reference', 'ServiceRequest'],
                            mds_path=Config.mds_path, patterns=Config.patterns)



    def test_basic_templating(self):
        for pattern in TestTemplating.templatize.get_patterns():
            cluster = ClusterManager.get_cluster(pattern)
            oppty_artifact = cluster.get_artifact_from_object(TestTemplating.templatize.get_objects()[0])
            oppty_artifact_xml = oppty_artifact.get_xml()
            token_map = oppty_artifact.get_tokens()
            template = cluster.get_template()
            opty_template_xml = copy.deepcopy(template)
            Util.substitute(opty_template_xml, token_map)
            self.assertEqual(oppty_artifact_xml, opty_template_xml)

    def test_token_filter(self):
        for pattern in TestTemplating.templatize.get_patterns():
            cluster = ClusterManager.get_cluster(TestTemplating.pattern)
            if cluster.consensus(Artifact.get_duplicate_tokens, Util.token_comparator) is False:
                print cluster
                self.assertTrue(False)

    def test_duplicate_token_filter(self):
        for pattern in TestTemplating.templatize.get_patterns():
            cluster = ClusterManager.get_cluster(pattern)
            cluster.get_processed_template()
            oppty_artifact = cluster.get_artifact_from_object(TestTemplating.templatize.get_objects()[0])
            oppty_artifact_xml = oppty_artifact.get_xml()
            token_map = oppty_artifact.get_tokens()
            template = cluster.get_template()
            oppty_template_xml = copy.deepcopy(template)
            Util.substitute(oppty_template_xml, token_map)
            self.assertEqual(oppty_artifact_xml, oppty_template_xml)

    def test_tokenization(self):
        for pattern in TestTemplating.templatize.get_patterns():
            cluster = ClusterManager.get_cluster(pattern)
            opty_artifact = cluster.get_artifact_from_object(TestTemplating.templatize.get_objects()[0])
            opty_template = opty_artifact.get_template()
            lead_artifact = cluster.get_artifact_from_object(TestTemplating.templatize.get_objects()[1])
            lead_template = lead_artifact.get_template()
            self.assertTrue(Util.element_tree_comparator(opty_template.getroot(), lead_template.getroot()))

    def test_basic_templating_generic(self):
        for pattern in TestTemplating.templatize.get_patterns():
            cluster = ClusterManager.get_cluster(pattern)
            for artifact in cluster.get_artifacts():
                artifact_xml = artifact.get_xml()
                token_map = artifact.get_tokens()
                template = cluster.get_template()
                artifact_template_xml = copy.deepcopy(template)
                Util.substitute(artifact_template_xml, token_map)
                if artifact_template_xml != artifact_template_xml:
                    print pattern
                    self.assertTrue(False)

    def test_duplicate_tokens_generic(self):
        for pattern in TestTemplating.templatize.get_patterns():
            cluster = ClusterManager.get_cluster(pattern)
            self.assertTrue(cluster.consensus(Artifact.get_duplicate_tokens, Util.token_comparator))

    def test_unique_tokens_generic(self):
        for pattern in TestTemplating.templatize.get_patterns():
            cluster = ClusterManager.get_cluster(pattern)
            self.assertTrue(cluster.consensus(Artifact.get_unique_tokens, Util.token_key_comparator))

    def test_tokenization_generic(self):
        for pattern in TestTemplating.templatize.get_patterns():
            cluster = ClusterManager.get_cluster(pattern)
            consensus, object = cluster.consensus(Artifact.get_template_root, Util.element_tree_comparator)
            if  consensus == False:
                print pattern
                print object
                self.assertTrue(False)


suite = unittest.TestLoader().loadTestsFromTestCase(TestTemplating)
unittest.TextTestRunner(verbosity=2).run(suite)