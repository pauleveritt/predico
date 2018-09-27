"""

A base class for services to implement.

"""
from dataclasses import dataclass


@dataclass
class BaseService:

    def get_injectables(self, request):
        # Extend the injectables from the service manager to include
        # the request and resource
        injectables = {k: v for (k, v) in self.sm.injectables.items()}
        injectables['Request'] = request
        injectables['Resource'] = request.resource

        return injectables
