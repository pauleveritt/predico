import dectate


class ResourceAction(dectate.Action):
    config = {
        'resources': dict
    }

    def __init__(self, name: str):
        super().__init__()
        self.name = name

    def identifier(self, resources):
        return self.name

    # noinspection PyMethodOverriding
    def perform(self, obj, resources):
        resources[self.name] = obj

    @classmethod
    def get_callbacks(cls, registry):
        # Presumes the registry has been committed

        q = dectate.Query('resource')
        return [args[1] for args in q(registry)]
