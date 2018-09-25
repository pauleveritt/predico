"""

A ServiceManager that manages registered services.

We need a single entry point for the various kinds of things we want
to do -- views, renderers, etc. This single entry point needs:

- Initial configuration

- State

- A way to discover and register services

- A way to retrieve services

"""
from typing import Dict

import dectate

from kaybee_component.injector import inject
from kaybee_component.registry import Registry
from kaybee_component.service.base_service import BaseService
from kaybee_component.service.configuration import ServiceManagerConfig


class InvalidInjectable(Exception):
    fmt = 'Invalid injectable type {type} requested from {klass}'


Services = Dict[str, BaseService]


class ServiceManager:
    config: ServiceManagerConfig
    registry: Registry
    services: Services

    def __init__(self,
                 config: ServiceManagerConfig,
                 registry: Registry
                 ):
        self.config = config
        self.registry = registry
        self.services = {}
        self.injectables = {}

    def initialize(self):
        """ Commit the actions and initialize the registry """
        dectate.commit(self.registry)

        # Get the injectables
        injectables = self.injectables

        # Stash ServiceManager stuff in injectables
        injectables[ServiceManagerConfig.__name__] = self.config,
        injectables[ServiceManager.__name__] = self

        # Make the Registry injectable
        injectables['Registry'] = self.registry

        # Make each service config available as injectable
        for serviceconfig in self.config.serviceconfigs.values():
            injectables[serviceconfig.__class__.__name__] = serviceconfig

        # Get a list of services
        q = dectate.Query('service')
        services = list(q(self.registry))

        # Go through each service, initialize it, then
        # put an instance in the service manager
        for action, target in services:
            # Place to build up the args passed into the dataclass
            args = {}

            # Use injector to make our target class
            props = dict()
            service = inject(props, injectables, target)

            # Store this in our dict of services
            name = action.name
            self.services[name] = service

            # Add this service, and its config, as injectable
            injectables[service.__class__.__name__] = service
