"""

Assemble all the pieces into an app that makes
requests and tests services, views, etc.

"""
from dataclasses import dataclass

import pytest

from kaybee_component import registry
from kaybee_component.service.configuration import ServiceManagerConfig
from kaybee_component.service.manager import ServiceManager, Services
from kaybee_component.services.request.config import RequestServiceConfig
from kaybee_component.services.resource.base_resource import Resource
from kaybee_component.services.resource.config import ResourceServiceConfig
from kaybee_component.services.resource.service import ResourceService
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
    """ Isolate the config of the ResourceService """

    config = ResourceServiceConfig(flag=99)
    return config


@pytest.fixture
def sm_config(
        resourceservice_config,
        requestservice_config,
        viewservice_config,
) -> ServiceManagerConfig:
    """ Gather each service's config into one for ServiceManager """

    config = ServiceManagerConfig(
        serviceconfigs=dict(
            resourceservice=resourceservice_config,
            requestservice=requestservice_config,
            viewservice=viewservice_config,
        )
    )
    return config


@pytest.fixture
def test_registry():
    """ Provide test isolation for builtin service registry """

    class TestServiceRegistry(registry):
        pass

    return TestServiceRegistry


@pytest.fixture
def uninitialized_sm(sm_config, test_registry) -> ServiceManager:
    """ Make a ServiceManager """

    sm = ServiceManager(sm_config, test_registry)
    return sm


# -------------------------------------------
# Registrations
#
# - Some view registrations
# - Some resource registrations
# - etc.
# -------------------------------------------

@pytest.fixture
def registrations():
    pass


@pytest.fixture
def initialized_sm(registrations, uninitialized_sm):
    """ The equivalent of an app with commit """
    uninitialized_sm.initialize()
    return uninitialized_sm
