import unittest
from Templatize import Templatize
from Config import Config
from ClusterManager import ClusterManager
from ArtifactManager import Artifact
from Util import Util
import copy
import xml.etree.ElementTree as ET


class TestTemplating(unittest.TestCase):

    def test_basic_templating(self):
        cluster = ClusterManager.get_cluster('VO.xml.xml')
        oppty_artifact = cluster.get_artifact_from_object('Opportunity')
        oppty_artifact_xml = oppty_artifact.get_xml()
        token_map = oppty_artifact.get_tokens()
        template = cluster.get_template()
        opty_template_xml = copy.deepcopy(template)
        Util.substitute(opty_template_xml, token_map)
        self.assertEqual(oppty_artifact_xml, opty_template_xml)

    def test_token_filter(self):
        cluster = ClusterManager.get_cluster('VO.xml.xml')
        self.assertTrue(cluster.consensus(Artifact.get_duplicate_tokens))

    def test_duplicate_token_filter(self):
        cluster = ClusterManager.get_cluster('VO.xml.xml')
        cluster.remove_duplicates_from_template()
        oppty_artifact = cluster.get_artifact_from_object('Opportunity')
        oppty_artifact_xml = oppty_artifact.get_xml()
        token_map = oppty_artifact.get_tokens()
        template = cluster.get_template()
        oppty_template_xml =  copy.deepcopy(template)
        Util.substitute(oppty_template_xml, token_map)
        self.assertEqual(oppty_artifact_xml, oppty_template_xml)

    def test_tokenization(self):
        cluster = ClusterManager.get_cluster('VO.xml.xml')
        opty_artifact = cluster.get_artifact_from_object('Opportunity')
        opty_template = opty_artifact.get_template()
        lead_artifact = cluster.get_artifact_from_object('Lead')
        lead_template = lead_artifact.get_template()
        self.assertEqual(ET.tostring(opty_template.getroot()), ET.tostring(lead_template.getroot()))

    def test_tokenization_generic(self):
        cluster = ClusterManager.get_cluster('VO.xml.xml')
        self.assertTrue(cluster.consensus(Artifact.get_serialized_template))

Templatize(debug=True, objects=['Lead', 'Opportunity', 'Note', 'Claim'], mds_path=Config.mds_path, patterns=['VO.xml.xml'])
suite = unittest.TestLoader().loadTestsFromTestCase(TestTemplating)
unittest.TextTestRunner(verbosity=2).run(suite)