import xml.etree.ElementTree as ET
from Config import Config

class XMLElement:
    def __init__(self, tag, attr = None, children = None):
        self.tag = tag
        self.attr = attr
        self.children = children

    def addChild(self, child):
        if self.children is None:
            self.children = []
        self.children.append(child)

    def addChildren(self, children):
        if self.children is None:
            self.children = children
        else:
            for child in children:
                self.children.append(child)


    def addAttr(self, att):
        if self.attr is None:
            self.attr = []
        self.attr.append(att)


    def getAttr(self):
        return self.attr

    def getChildren(self):
        return self.children



class Pair:
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def getKey(self):
        return self.key
    def getValue(self):
        return self.value


class Artifact:
    def __init__(self, path, fp = None, xml_element_tree = None, sorted_path = None):
        self.path = path
        self.fp = fp
        self.xml_element_tree = xml_element_tree
        self.sorted_path = sorted_path

    def sort(self):
        if self.xml_element_tree is None:
            self.xml_element_tree = ET.parse(Config.mds_path + '/' + self.path)

        tree = self.xml_element_tree
        xml_root = self.parse(tree.getroot())
        self.printXML(xml_root, 0)


    def printXML(self, xml_elem, tab):

        for i in range(tab):
            print "\t",

        print "<" + xml_elem.tag,


        if xml_elem.getAttr() is not None:
            for v in xml_elem.getAttr():
                print "key-" , v.getKey(), "value-", v.getValue(),


        print ">"

        if xml_elem.getChildren() is not None:
            for child in xml_elem.getChildren():
                self.printXML(child, tab+1)

        for i in range(tab):
            print "\t",

        print "</" + xml_elem.tag + ">"




    def parse(self, root):

        root_tag = root.tag
        root_attr = root.attrib
        children = root.getchildren()

        xml_elem = XMLElement(root_tag)
        sorted_keys = sorted(root_attr.keys())
        for k in sorted_keys:
            xml_elem.addAttr(Pair(k, root_attr[k]))

        if len(children) == 0:
            return xml_elem

        xml_children = []
        for child in children:
            xml_children.append(self.parse(child))

        xml_children = sorted(xml_children, key = lambda x: x.tag)
        xml_elem.addChildren(xml_children)

        return xml_elem



