import xml.etree.ElementTree as ET
import copy
from Util import Util

class Artifact:
    def __init__(self, path):
        self.path = path
        self.fp = None
        self.et = ET.parse(self.path)
        self.xml = self.sort(self.et.getroot())
        self.tokens = {}
        self.unique_tokens = None
        self.value_to_token = None
        self.cluster = None

    def get_path(self):
        return self.path

    def set_cluster(self, cluster):
        self.cluster = cluster

    def add_token(self, name, value):
        self.tokens[name] = value

    def get_tokens(self):
        return self.tokens

    """
        This method returns a dictionary where each key,value pair in the 
        dictionary siginifies that the token "key" is a duplicate of token "value"
        and hence all occurences of token "key" should be replaced by token "value" in
        the template xml
    """
    def get_duplicate_tokens(self):
        tokens = self.get_tokens()
        token_names = sorted(tokens.keys())
        value_to_token_name = {}
        ans = {}
        for token_name in token_names:
            token_value = tokens[token_name]
            if token_value in value_to_token_name:
                ans[token_name] = value_to_token_name[token_value]
            else:
                value_to_token_name[token_value] = token_name
        return ans

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

    def get_cluster(self):
        return self.cluster

    def get_template(self):
        et = self.et
        dup_tokens = self.get_cluster().get_duplicate_tokens()
        unique_tokens = {}
        all_tokens = self.get_tokens()

        for token in all_tokens:
            if token not in dup_tokens:
                unique_tokens[token] = all_tokens[token]
        self.unique_tokens = unique_tokens

        value_to_token = {}
        for token in unique_tokens:
            value_to_token[unique_tokens[token]] = token
        self.value_to_token = value_to_token

        et = copy.deepcopy(self.et)
        Util.tokenize(et.getroot(), value_to_token)
        return et



class XMLElement:
    def __init__(self, tag, attr=None, children=None):
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

    def __eq__(self, other):
        if isinstance(other, XMLElement):
            if self.tag != other.tag:
                return False

            self_attr = self.get_attr()
            other_attr = other.get_attr()

            if self_attr != other_attr:
                return False

            self_children = self.get_children()
            other_children = other.get_children()

            for sc, oc in zip(self_children or [], other_children or []):
                if sc != oc:
                    return False

            return True

        return NotImplemented

    def __ne__(self, other):
        return not self == other

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

    def set_value(self, value):
        if value is None:
            raise Exception("None value set for pair")
        self.value = value

    def __eq__(self, other):
        if isinstance(other, Pair):
            if other.get_key() == self.get_key() and self.get_value() == other.get_value():
                return True
            return False
        return NotImplemented


class ArtifactManager:

    path_to_artifact = {}

    @staticmethod
    def get_artifact(path):
        if path not in ArtifactManager.path_to_artifact:
            ArtifactManager.path_to_artifact[path] = Artifact(path)

        return ArtifactManager.path_to_artifact[path]