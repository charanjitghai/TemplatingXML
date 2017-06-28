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
