"""

A ServiceManager that manages registered services.

We need a single entry point for the various kinds of things we want
to do -- views, renderers, etc. This single entry point needs:

- Initial configuration

- State

- A way to discover and register services

- A way to retrieve services

"""

from kaybee_component.service.configuration import ServiceManagerConfig
from tests.unit.service.registry import ServiceRegistry


class ServiceManager:
    config: ServiceManagerConfig
    registry: ServiceRegistry

    def __init__(self,
                 config: ServiceManagerConfig,
                 registry: ServiceRegistry,
                 ):
        self.config = config
        self.registry = registry
