from dataclasses import dataclass

import dectate
import pytest

from kaybee_component import registry
from kaybee_component.service.action import ServiceAction
from kaybee_component.service.configuration import ServiceManagerConfig
from kaybee_component.service.manager import ServiceManager
from kaybee_component.services.request.config import RequestServiceConfig
from kaybee_component.services.view.base_view import IndexView
from kaybee_component.services.view.config import ViewServiceConfig
from kaybee_component.services.view.service import setup as viewservice_setup


@pytest.fixture
def viewservice_config() -> ViewServiceConfig:
    config = ViewServiceConfig(flag=99)
    return config


@pytest.fixture
def requestservice_config() -> RequestServiceConfig:
    config = RequestServiceConfig(flag=99)
    return config


@pytest.fixture
def sm_config(viewservice_config, requestservice_config) -> ServiceManagerConfig:
    """ Gather service's config into one for ServiceManager """

    config = ServiceManagerConfig(
        serviceconfigs=dict(
            viewservice=viewservice_config,
            requestservice=requestservice_config,
        )
    )
    return config


@pytest.fixture
def sm_registry():
    """ Provide test isolation for builtin service registry """

    class TestServiceRegistry(dectate.App):
        service = dectate.directive(ServiceAction)

    return TestServiceRegistry


@pytest.fixture
def sm(sm_config, sm_registry) -> ServiceManager:
    """ Make a ServiceManager """

    sm = ServiceManager(sm_config, sm_registry)
    sm.registry = sm_registry
    return sm


@pytest.fixture
def register_services(sm_registry):
    """ Configure the well-known services """
    viewservice_setup(sm_registry)


# -------------------------------------------
# Registrations
#
# - Some view registrations
# - Some resource registrations
# - etc.
# -------------------------------------------

@pytest.fixture
def test_registry():
    """ Provide an isolated registry """

    class TestRegistry(registry):
        pass

    return TestRegistry


@pytest.fixture
def for_view1(test_registry):
    @test_registry.view(for_=IndexView)
    @dataclass
    class ForView1:
        name: str = 'For View One'


@pytest.fixture
def registrations(for_view1):
    return


@pytest.fixture
def initialized_sm(register_services, registrations, sm):
    """ The equivalent of an app with commit """
    sm.initialize()
    return sm
