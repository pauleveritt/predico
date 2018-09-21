"""

Dectate action for registering services.

"""
import dectate


class ServiceAction(dectate.Action):
    config = {
        'services': dict
    }

    def __init__(self, name):
        self.name = name

    def identifier(self, services):
        return self.name

    def perform(self, obj, services):
        services[self.name] = obj
