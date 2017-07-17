from Config import Config
from xml.etree.ElementTree import Element

class Util:

    @staticmethod
    def substitute(template, tokens):
        token_string = Config.token_string
        for attr in template.get_attr() or []:
            if attr.get_value().startswith(token_string) and attr.get_value() in tokens:
                attr.set_value(tokens[attr.get_value()])

        for child in template.get_children() or []:
            Util.substitute(child, tokens)

    @staticmethod
    def substitute_et(template, tokens):
        token_string = Config.token_string
        for attr in template.getattrib() or {}:
            value = template.getattrib[attr]
            if value.startswith(token_string) and value in tokens:
                template.getattrib[attr] = tokens[value]

        for child in template.getchildren() or []:
            Util.substitute(child, tokens)

    @staticmethod
    def get_element_from_xml(xml_elem):
        if xml_elem is None:
            return None
        root_elem = Element(xml_elem.get_tag())
        attributes = xml_elem.get_attr()
        for attr in attributes or []:
            root_elem.set(attr.get_key(), attr.get_value())

        for child in xml_elem.get_children() or []:
            child_elem = Util.get_element_from_xml(child)
            root_elem.getchildren().append(child_elem)

        return root_elem

    @staticmethod
    def tokenize(root, value_to_token):
        root_tag = root.tag
        root_attr = root.attrib
        children = root.getchildren()

        for attr in root_attr or {}:
            value = root_attr[attr]
            if value in value_to_token:
                root.set(attr, value_to_token[value])

        for child in children:
            Util.tokenize(child, value_to_token)

    @staticmethod
    def token_key_comparator(token_map1, token_map2):
        return token_map1.keys() == token_map2.keys()

    @staticmethod
    def token_comparator(token_map1, token_map2):
        return token_map1 == token_map2

    @staticmethod
    def element_tree_comparator(root1, root2):
        if root1.tag != root2.tag:
            return False
        if root1.attrib != root2.attrib:
            return False

        root1_children = root1.getchildren()
        root2_children = root2.getchildren()

        if root1_children is None:
            if root2_children is not None:
                return False

        if root2_children is None:
            if root1_children is not None:
                return False

        if len(root1_children) != len(root2_children):
            return False

        for c1, c2 in zip(root1_children, root2_children):
            if Util.element_tree_comparator(c1, c2) == False:
                return False

        return True

    """
        this method tokenizes 2 strings i.e. will extract the common
        part of the strings and replace the different parts with tokens
        for example:
            string1: OptypersdefCommonOpportunityQue
            string2: LedpersdefCommonLeadQue
            should return $token1$persdefCommon$token2$Que
            
        it's assumed that the strings won't contain character: "$"
        
        first version of the code will just check for common prefix and suffix.
    """
    @staticmethod
    def tokenize_strings(string1, string2):

        s = 0
        while s < len(string1) and s < len(string2) and string1[s] == string2[s]:
            s += 1

        prefix = string1[:s]


        e1 = len(string1) -1
        e2 = len(string2) -1
        while e1 >=0 and e2 >=0 and string1[e1] == string2[e2]:
            e1 -= 1
            e2 -= 1

        suffix = string1[-e1]

        return prefix, suffix



class string_token:
    def __init__(self, idx, value, is_token):
        self.idx = idx
        self.value = value
        self.is_token = is_token

    def get_value(self):
        return self.value

    def get_is_token(self):
        return self.is_token

    def get_idx(self):
        return self.idx


class tokenized_string():

    def __init__(self):
        self.string_tokens = []

    def sort_tokens(self):
        self.string_tokens.sort(key=lambda x: x.idx)
        return self.string_tokens

    def add_string_token(self, token_string):
        self.string_tokens.append(token_string)

    def get_string(self):
        return "".join(self.sort_tokens())

