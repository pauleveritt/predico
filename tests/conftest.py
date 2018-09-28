"""

Assemble all the pieces into an app that makes
requests and tests services, views, etc.

"""

import pytest

from predico import registry
from predico.servicemanager.configuration import ServiceManagerConfig
from predico.servicemanager.manager import ServiceManager
from predico.services.adapter.config import AdapterServiceConfig
from predico.services.request.config import RequestServiceConfig
from predico.services.resource.config import ResourceServiceConfig
from predico.services.view.config import ViewServiceConfig


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
def adapterservice_config() -> AdapterServiceConfig:
    """ Isolate the config of the AdapterService """

    config = AdapterServiceConfig(flag=99)
    return config


@pytest.fixture
def sm_config(
        adapterservice_config,
        resourceservice_config,
        requestservice_config,
        viewservice_config,
) -> ServiceManagerConfig:
    """ Gather each service's config into one for ServiceManager """

    config = ServiceManagerConfig(
        serviceconfigs=dict(
            adapterservice=adapterservice_config,
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
