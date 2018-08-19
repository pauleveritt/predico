"""

Dectate app for registering services.

This is not a registry for all kinds of everything. It only knows about
service actions, not views, renderers, etc. Each of those have a service
with manages their registrations.

"""
import dectate


class RequestAction(dectate.Action):
    config = {
        'requests': dict
    }

    def __init__(self, name):
        super().__init__()
        self.name = name

    def identifier(self, requests):
        return self.name

    def perform(self, obj, requests):
        requests[self.name] = obj


class BaseRequestRegistry(dectate.App):
    request = dectate.directive(RequestAction)

