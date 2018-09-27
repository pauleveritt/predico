from dataclasses import dataclass
from typing import Type

import pytest

from kaybee_component.registry import Registry
from kaybee_component.servicemanager.base_service import BaseService
from kaybee_component.servicemanager.configuration import ServiceManagerConfig
from kaybee_component.servicemanager.manager import ServiceManager
from kaybee_component.services.request.config import RequestServiceConfig
from kaybee_component.services.resource.config import ResourceServiceConfig
from kaybee_component.services.view.config import ViewServiceConfig


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
def resourceservice_config() -> ResourceServiceConfig:
    """ Isolate the config of the RequestService """

    config = ResourceServiceConfig(flag=99)
    return config


@pytest.fixture
def sm_config(
        viewservice_config,
        requestservice_config,
        resourceservice_config,
) -> ServiceManagerConfig:
    """ Gather each service's config into one for ServiceManager """

    config = ServiceManagerConfig(
        serviceconfigs=dict(
            viewservice=viewservice_config,
            requestservice=requestservice_config,
            resourceservice=resourceservice_config,
        )
    )
    return config


@pytest.fixture
def test_registry():
    """ Make an isolated registry for testing"""

    class TestServiceRegistry(Registry):
        pass

    return TestServiceRegistry


@pytest.fixture
def uninitialized_sm(sm_config, test_registry) -> ServiceManager:
    """ Make a ServiceManager """

    sm = ServiceManager(sm_config, test_registry)
    return sm


@pytest.fixture
def initialized_sm(uninitialized_sm):
    uninitialized_sm.initialize()
    return uninitialized_sm


@pytest.fixture
def invalid_injectable_type(test_registry) -> Type[BaseService]:
    class BogusType:
        pass

    @test_registry.service(name='view')
    @dataclass(frozen=True)
    class InvalidService(BaseService):
        sm_config: BogusType

    return InvalidService
