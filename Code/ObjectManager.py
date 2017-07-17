class ObjectManager:

    obj_name_to_obj = {}

    @staticmethod
    def get_obj(obj_name):
        if obj_name not in ObjectManager.obj_name_to_obj:
            obj = Object(obj_name)
            ObjectManager.obj_name_to_obj[obj_name] = obj
        return ObjectManager.obj_name_to_obj[obj_name]


class Object:
    def __init__(self, obj_name):
        self.obj_name = obj_name
        self.artifacts = []
        self.all_tokens = None
    def add_artifact(self, artifact):
        self.artifacts.append(artifact)

    def get_artifacts(self):
        return self.artifacts

    def get_name(self):
        return self.obj_name

    def get_all_tokens(self):
        if self.all_tokens is None:
            self.all_tokens = {k:v for artifact in self.get_artifacts() for k,v in artifact.get_unique_tokens().items()}
        return self.all_tokens