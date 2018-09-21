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

from kaybee_component.registry import Registry
from kaybee_component.service.base_service import BaseService
from kaybee_component.service.configuration import ServiceManagerConfig
from kaybee_component.services.request.action import RequestAction
from kaybee_component.services.view.action import ViewAction


class InvalidInjectable(Exception):
    fmt = 'Invalid injectable type {type} requested from {klass}'


class ServiceManager:
    config: ServiceManagerConfig
    registry: Registry
    services: Dict[str, BaseService]

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

        # TODO Introspect the other actions instead of hardwiring
        serviceconfigs = self.config.serviceconfigs
        injectables['ViewAction'] = ViewAction
        injectables['ViewServiceConfig'] = serviceconfigs['viewservice']
        injectables['RequestAction'] = RequestAction
        injectables['RequestServiceConfig'] = serviceconfigs['requestservice']
        injectables['Registry'] = self.registry

        # Get a list of services
        q = dectate.Query('service')
        services = list(q(self.registry))

        # Go through each service, initialize it, then
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
                    value = getattr(type_, attr_)
                    args[field_name] = value

            service = target(**args)
            name = action.name
            self.services[name] = service

            # Add this service, and its config, as injectable
            injectables[service.__class__.__name__] = service
