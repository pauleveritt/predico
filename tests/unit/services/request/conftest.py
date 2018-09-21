from dataclasses import dataclass

import dectate
import pytest

from kaybee_component import RequestAction
from kaybee_component.service.configuration import ServiceManagerConfig
from kaybee_component.service.manager import ServiceManager
from kaybee_component.service.registry import services
from kaybee_component.services.request.config import RequestServiceConfig
from kaybee_component.services.request.service import RequestService


@pytest.fixture
def rs_config() -> RequestServiceConfig:
    config = RequestServiceConfig(flag=99)
    return config


@pytest.fixture
def rs_registry():
    class TestRequestServiceRegistry(dectate.App):
        request = dectate.directive(RequestAction)

    return TestRequestServiceRegistry


@pytest.fixture
def rs(rs_config, rs_registry) -> RequestService:
    service = RequestService(rs_registry, rs_config)
    return service


@pytest.fixture
def sm_config(rs_config) -> ServiceManagerConfig:
    config = ServiceManagerConfig(
        serviceconfigs=dict(
            requestservice=rs_config,
        )
    )
    return config


@pytest.fixture
def sm_registry():
    # Provide test isolation by making a local subclass which is
    # blown away on each test run
    class TestServiceRegistry(services):
        pass

    return TestServiceRegistry


@pytest.fixture
def sm(sm_config, sm_registry) -> ServiceManager:
    sm = ServiceManager(sm_config)
    sm.registry = sm_registry
    return sm


@pytest.fixture
def register_service(sm_registry):
    @sm_registry.service(name='request')
    @dataclass(frozen=True)
    class TestRequestService(RequestService):
        pass


@pytest.fixture
def initialized_sm(register_service, sm):
    sm.initialize()
    return sm
