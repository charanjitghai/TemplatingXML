import xml.etree.ElementTree as ET


class Artifact:
    def __init__(self, path):
        self.path = path
        self.fp = None
        self.xml = self.sort(ET.parse(self.path).getroot())
        self.tokens = {}
        self.cluster = None


    def set_cluster(self, cluster):
        self.cluster = cluster

    def add_token(self, name, value):
        self.tokens[name] = value


    def get_fp(self):
        if self.fp is None:
            self.fp = open(self.path, 'r')
        return self.fp


    def get_xml(self):
        return self.xml

    def print_xml(self):
        self.xml.print_xml()

    def sort(self, root):

        root_tag = root.tag
        root_attr = root.attrib
        children = root.getchildren()

        xml_elem = XMLElement(root_tag)
        sorted_keys = sorted(root_attr.keys())
        for k in sorted_keys:
            xml_elem.add_attr(Pair(k, root_attr[k]))

        if len(children) == 0:
            return xml_elem

        xml_children = []
        for child in children:
            xml_children.append(self.sort(child))

        xml_children.sort()
        xml_elem.add_children(xml_children)

        return xml_elem


class XMLElement:
    def __init__(self, tag, attr = None, children = None):
        self.tag = tag
        self.attr = attr
        self.children = children

    def add_child(self, child):
        if self.children is None:
            self.children = []
        self.children.append(child)

    def add_children(self, children):
        if self.children is None:
            self.children = children
        else:
            for child in children:
                self.children.append(child)


    def add_attr(self, att):
        if self.attr is None:
            self.attr = []
        self.attr.append(att)


    def get_attr(self):
        return self.attr
    def get_children(self):
        return self.children
    def get_tag(self):
        return self.tag


    def __lt__(self, other):
        if isinstance(other, XMLElement):

            if other.tag > self.tag:
                return True
            if self.tag > other.tag:
                return False


            self_attr = self.get_attr()
            other_attr = other.get_attr()
            if self_attr is None:
                return True
            if other_attr is None:
                return False
            if len(other_attr) > len(self_attr):
                return True
            if len(self_attr) > len(other_attr):
                return False


            self_children = self.get_children()
            other_children = other.get_children()
            if self_children is None:
                return True
            if other_children is None:
                return False
            if len(other_children) > len(self_children):
                return True
            if len(self_children) > len(other_children):
                return False


            for s,o in zip(self_attr, other_attr):
                if s.get_key() < o.get_key():
                    return True
                if s.get_key() > o.get_key():
                    return False

                if s.get_value() < o.get_value():
                    return True
                if s.get_value() > o.get_value():
                    return False


            for s,o in zip(self_children, other_children):
                if s < o:
                    return True
                if s > o:
                    return False

            return False

        return NotImplemented


    def print_xml(self):
        self.print_xml_tab(0)

    def print_xml_tab(self, tab):

        xml_elem = self

        for i in range(tab):
            print "\t",

        print "<" + xml_elem.tag,


        if xml_elem.get_attr() is not None:
            for v in xml_elem.get_attr():
                print "key-" , v.get_key(), "value-", v.get_value(),


        print ">"

        if xml_elem.get_children() is not None:
            for child in xml_elem.get_children():
                child.print_xml_tab(tab + 1)

        for i in range(tab):
            print "\t",

        print "</" + xml_elem.tag + ">"


class Pair:
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def get_key(self):
        return self.key
    def get_value(self):
        return self.value

