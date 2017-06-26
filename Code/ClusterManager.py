from ArtifactManager import XMLElement, Pair
from Config import Config

class Cluster:
    def __init__(self, name):
        self.name = name
        self.artifacts = []
        self.template = None
        self.n_token = 0

    def get_artifact_from_object(self, object):
        for artifact in self.artifacts:
            if object in artifact.get_path():
                return artifact
        return None

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.name == other.name
        return False

    def __hash__(self):
        return hash(self.name)

    def add_artifact(self, file):
        self.artifacts.append(file)

    def get_artifacts(self):
        return self.artifacts

    def get_template(self):
        if self.template is None:
            self.template = self.process(
                [artifact.get_xml() for artifact in self.artifacts],
                self.artifacts
            )
        return self.template

    def process(self, xmls, artifacts):
        tag = xmls[0].get_tag()
        ans = XMLElement(tag)

        for xml in xmls[1:]:
            c_tag = xml.get_tag()
            if c_tag != tag:
                raise Exception("tags not matched, expected " + tag + " found " + c_tag)

        all_tokens = []
        c_attrs = xmls[1].get_attr()
        attrs = xmls[0].get_attr()
        mismatch_keys = []
        if attrs is not None:
            for attr, c_attr in zip(attrs, c_attrs):
                if attr.get_value() != c_attr.get_value():
                    mismatch_keys.append(attr.get_key())
                    token = Config.token_string + str(self.n_token)
                    all_tokens.append(token)
                    self.n_token += 1
                    ans.add_attr(Pair(attr.get_key(), token))
                else:
                    ans.add_attr(Pair(attr.get_key(), attr.get_value()))

            for artifact,xml in zip(artifacts, xmls):
                c_attrs = xml.get_attr()
                token_idx = 0
                for attr, c_attr in zip(attrs, c_attrs):
                    if attr.get_key() != c_attr.get_key():
                        raise Exception("keys not matched, expected " + attr.get_key() + " found " + c_attr.get_key())
                    if attr.get_key() in mismatch_keys:
                        artifact.add_token(all_tokens[token_idx], c_attr.get_value())
                        token_idx += 1

        if xmls[0].get_children() is not None:
            all_children = {}
            for i in range(len(xmls[0].get_children())):
                for j in range(len(xmls)):
                    if i not in all_children:
                        all_children[i] = []
                    all_children[i].append(xmls[j].get_children()[i])

            for i in range(len(xmls[0].get_children())):
                child_template = self.process(all_children[i], artifacts)
                ans.add_child(child_template)

        return ans


class ClusterManager:
    pattern_to_cluster = {}

    @staticmethod
    def get_cluster(pattern):
        if pattern not in ClusterManager.pattern_to_cluster:
            ClusterManager.pattern_to_cluster[pattern] = Cluster(pattern)
        return ClusterManager.pattern_to_cluster[pattern]
