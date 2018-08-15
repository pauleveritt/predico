import dectate

from kaybee_component.views import ViewAction


class ServiceAction(dectate.Action):
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


class AdapterAction(dectate.Action):
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


class Kaybee(dectate.App):
    view = dectate.directive(ViewAction)
    service = dectate.directive(ServiceAction)
    adapter = dectate.directive(AdapterAction)
