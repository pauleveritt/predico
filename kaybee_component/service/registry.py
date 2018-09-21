"""

Dectate app for registering services.

This is not a registry for all kinds of everything. It only knows about
service actions, not views, renderers, etc. Each of those have a service
with manages their registrations.

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


class services(dectate.App):
    service = dectate.directive(ServiceAction)
