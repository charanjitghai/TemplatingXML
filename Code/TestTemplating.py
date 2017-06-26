import unittest
from Templatize import Templatize
from Config import Config
from ClusterManager import ClusterManager
from Util import Util
import copy

class TestTemplating(unittest.TestCase):
    def test_basic_templating(self):
        templatize = Templatize(debug=True, objects=['Lead', 'Opportunity'], mds_path=Config.mds_path, patterns=['VO.xml.xml'])
        cluster = ClusterManager.get_cluster('VO.xml.xml')
        oppty_artifact = cluster.get_artifact_from_object('Opportunity')
        oppty_artifact_xml = oppty_artifact.get_xml()
        token_map = oppty_artifact.get_tokens()
        template = cluster.get_template()
        opty_template_xml = copy.deepcopy(template)
        Util.substitute(opty_template_xml, token_map)
        self.assertEqual(oppty_artifact_xml, opty_template_xml)

suite = unittest.TestLoader().loadTestsFromTestCase(TestTemplating)
unittest.TextTestRunner(verbosity=2).run(suite)