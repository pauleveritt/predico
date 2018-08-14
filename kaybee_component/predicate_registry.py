import dectate


class PluginAction(dectate.Action):
    config = {
        'plugins': dict
    }

    def __init__(self, name):
        super().__init__()
        self.name = name

    def identifier(self, plugins):
        return self.name

    def perform(self, obj, plugins=None):
        if plugins is None:
            plugins = []
        plugins[self.name] = obj


class PluginApp(dectate.App):
    plugin = dectate.directive(PluginAction)
