from Templatize import Templatize
from Config import Config
from ObjectManager import ObjectManager

templatize = Templatize(debug=True, objects=['Opportunity', 'Lead', 'Note', 'Contact', 'Deal', 'BudgetFundRequest', 'SalesObjective', 'TerritoryResource', 'ActivityAssignee',
            'BusinessPlan', 'DealProduct', 'OpportunityRevenuePartner', 'Reference', 'ServiceRequest'], mds_path=Config.mds_path, patterns=Config.patterns)

for obj_name in templatize.objects:
    object = ObjectManager.get_obj(obj_name)
    artifacts = object.get_artifacts()
    print "Object " + obj_name
    for artifact in artifacts:
        print "\t" + artifact.get_path()

    print artifacts[2].get_template().getroot().attrib
    print artifacts[2].get_tokens()

