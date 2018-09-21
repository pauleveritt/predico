from dataclasses import dataclass, field
from typing import Type

import dectate
import pytest

from kaybee_component.service.action import ServiceAction
from kaybee_component.service.base_service import BaseService
from kaybee_component.service.configuration import ServiceManagerConfig
from kaybee_component.service.manager import ServiceManager
from kaybee_component.services.request.config import RequestServiceConfig
from kaybee_component.services.request.service import \
    setup as requestservice_setup
from kaybee_component.services.view.config import ViewServiceConfig
from kaybee_component.services.view.service import setup as viewservice_setup


# -------------------------------------------
# Service Manager
#
# - Get configurations for each of the configured services,
# - Combine into the ServiceManagerConfig
# - Use that to bootstrap the ServiceManager
#
# -------------------------------------------

@pytest.fixture
def viewservice_config() -> ViewServiceConfig:
    """ Isolate the config of the ViewService """

    config = ViewServiceConfig(flag=99)
    return config


@pytest.fixture
def requestservice_config() -> RequestServiceConfig:
    """ Isolate the config of the RequestService """

    config = RequestServiceConfig(flag=99)
    return config


@pytest.fixture
def sm_config(
        viewservice_config,
        requestservice_config) -> ServiceManagerConfig:
    """ Gather each service's config into one for ServiceManager """

    config = ServiceManagerConfig(
        serviceconfigs=dict(
            viewservice=viewservice_config,
            requestservice=requestservice_config,
        )
    )
    return config


@pytest.fixture
def sm_registry():
    """ Make a registry solely for services, one single action """

    # Provide test isolation by making a local subclass which is
    # blown away on each test run
    class TestServiceRegistry(dectate.App):
        service = dectate.directive(ServiceAction)

    return TestServiceRegistry


@pytest.fixture
def sm(sm_config, sm_registry) -> ServiceManager:
    """ Make a ServiceManager """

    sm = ServiceManager(sm_config, sm_registry)
    sm.registry = sm_registry
    return sm


# -------------------------------------------
# Services
#
# - Take the well-known services and configure them
# -------------------------------------------

@pytest.fixture
def register_services(sm_registry):
    requestservice_setup(sm_registry)
    viewservice_setup(sm_registry)


@pytest.fixture
def initialized_sm(sm):
    sm.initialize()
    return sm


@pytest.fixture
def invalid_injectable_type(sm_registry) -> Type[BaseService]:
    class BogusType:
        pass

    @sm_registry.service(name='view')
    @dataclass(frozen=True)
    class InvalidService(BaseService):
        sm_config: BogusType = field(
            metadata=dict(
                injected=True
            )
        )

    return InvalidService
