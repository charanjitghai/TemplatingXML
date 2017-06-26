from Config import Config
class Util:

    @staticmethod
    def substitute(template, tokens):
        token_string = Config.token_string
        for attr in template.get_attr() or []:
            if attr.get_value().startswith(token_string):
                attr.set_value(tokens[attr.get_value()])

        for child in template.get_children() or []:
            Util.substitute(child, tokens)