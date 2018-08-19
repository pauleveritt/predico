"""

A ServiceManager that manages registered services.

We need a single entry point for the various kinds of things we want
to do -- views, renderers, etc. This single entry point needs:

- Initial configuration

- State

- A way to discover and register services

- A way to retrieve services

"""
from dataclasses import fields
from typing import Dict

import dectate

from kaybee_component.service.base_service import BaseService
from kaybee_component.service.configuration import ServiceManagerConfig
from tests.unit.service.registry import ServiceRegistry


class InvalidInjectable(Exception):
    fmt = 'Invalid injectable type {type} requested from {klass}'


class ServiceManager:
    config: ServiceManagerConfig
    registry: ServiceRegistry
    services: Dict[str, BaseService]

    def __init__(self,
                 config: ServiceManagerConfig,
                 registry: ServiceRegistry,
                 ):
        self.config = config
        self.registry = registry
        self.services = {}

    @property
    def injectables(self):
        """ Provide a mapping of what this container can inject

        The keys are the type information the consumer will ask for. The
        values are what to pass in.

        """

        _injectables = {
            self.config.__class__.__name__: self.config,
        }

        # For convenience, allow each configured service's configs
        # to be in the top level
        for config in self.config.serviceconfigs.values():
            _injectables[config.__class__.__name__] = config

        return _injectables

    def initialize(self):
        """ Commit the actions and initialize services """
        dectate.commit(self.registry)

        # Get a list of services
        query = dectate.Query('service')
        services = list(query(self.registry))

        # Get the injectables
        injectables = self.injectables

        # Go through each service, initialize it, commit, then
        # put an instance in the service manager
        for action, target in services:
            # Place to build up the args passed into the dataclass
            args = {}

            # Inspect target dataclass and find what it wants injected
            for field in fields(target):
                field_name = field.name

                if field.metadata.get('injected', False):
                    # Sucks that we have to use strings for keys, instead
                    # of actual classes
                    field_type = field.type.__name__

                    # If we don't have this value in the injectables,
                    # raise a custom exception
                    injected_value = injectables.get(field_type, False)
                    if injected_value is False:
                        fmt = InvalidInjectable.fmt
                        msg = fmt.format(
                            type=field_type,
                            klass=self.__class__.__name__
                        )
                        raise InvalidInjectable(msg)

                    # Add this to the arguments we are providing to
                    # construct the dataclass
                    args[field_name] = injectables[field_type]

                elif field.metadata.get('injectedattr', False):
                    injectedattr = field.metadata['injectedattr']
                    field_type = injectedattr['type_'].__name__

                    # If we don't have this value in the injectables,
                    # raise a custom exception
                    injected_value = injectables.get(field_type, False)
                    if injected_value is False:
                        fmt = InvalidInjectable.fmt
                        msg = fmt.format(
                            type=field_type,
                            klass=self.__class__.__name__
                        )
                        raise InvalidInjectable(msg)

                    # Add this to the arguments we are providing to
                    # construct the dataclass
                    type_ = injectables[field_type]
                    attr_ = injectedattr['attr']
                    value = getattr(type_, attr_, False)
                    if not value:
                        # Raise an exception
                        pass
                    args[field_name] = value

            service = target(**args)
            name = action.name
            self.services[name] = service
