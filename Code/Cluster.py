class Cluster:
    def __init__(self, name):
        self.name = name
        self.artifacts = []

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