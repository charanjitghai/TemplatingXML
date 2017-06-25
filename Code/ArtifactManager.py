from Artifact import Artifact

class ArtifactManager:

    path_to_artifact = {}

    @staticmethod
    def get_artifact(path):
        if path not in ArtifactManager.path_to_artifact:
            ArtifactManager.path_to_artifact[path] = Artifact(path)

        return ArtifactManager.path_to_artifact[path]