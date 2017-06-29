from Config import Config
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
