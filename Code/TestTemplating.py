import unittest
from Templatize import Templatize
from Config import Config
from ClusterManager import ClusterManager
from ArtifactManager import Artifact
from Util import Util
import copy
import xml.etree.ElementTree as ET


class TestTemplating(unittest.TestCase):

    pattern = 'AttrBundle.xlf.xml'
    templatize = Templatize(debug=True, objects=['Lead', 'Opportunity', 'Claim'], mds_path=Config.mds_path, patterns=[pattern])

    def test_basic_templating(self):
        for pattern in TestTemplating.templatize.get_patterns():
            cluster = ClusterManager.get_cluster(pattern)
            oppty_artifact = cluster.get_artifact_from_object('Opportunity')
            oppty_artifact_xml = oppty_artifact.get_xml()
            token_map = oppty_artifact.get_tokens()
            template = cluster.get_template()
            opty_template_xml = copy.deepcopy(template)
            Util.substitute(opty_template_xml, token_map)
            self.assertEqual(oppty_artifact_xml, opty_template_xml)

    def test_token_filter(self):
        for pattern in TestTemplating.templatize.get_patterns():
            cluster = ClusterManager.get_cluster(TestTemplating.pattern)
            self.assertTrue(cluster.consensus(Artifact.get_duplicate_tokens, Util.token_comparator))

    def test_duplicate_token_filter(self):
        for pattern in TestTemplating.templatize.get_patterns():
            cluster = ClusterManager.get_cluster(pattern)
            cluster.remove_duplicates_from_template()
            oppty_artifact = cluster.get_artifact_from_object('Opportunity')
            oppty_artifact_xml = oppty_artifact.get_xml()
            token_map = oppty_artifact.get_tokens()
            template = cluster.get_template()
            oppty_template_xml =  copy.deepcopy(template)
            Util.substitute(oppty_template_xml, token_map)
            self.assertEqual(oppty_artifact_xml, oppty_template_xml)

    def test_tokenization(self):
        for pattern in TestTemplating.templatize.get_patterns():
            cluster = ClusterManager.get_cluster(pattern)
            opty_artifact = cluster.get_artifact_from_object('Opportunity')
            opty_template = opty_artifact.get_template()
            lead_artifact = cluster.get_artifact_from_object('Lead')
            lead_template = lead_artifact.get_template()
            self.assertTrue(Util.element_tree_comparator(opty_template.getroot(), lead_template.getroot()))

    def test_tokenization_generic(self):
        for pattern in TestTemplating.templatize.get_patterns():
            cluster = ClusterManager.get_cluster(pattern)
            print pattern
            self.assertTrue(cluster.consensus(Artifact.get_template_root, Util.element_tree_comparator))


suite = unittest.TestLoader().loadTestsFromTestCase(TestTemplating)
unittest.TextTestRunner(verbosity=2).run(suite)