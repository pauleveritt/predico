import pytest

from kaybee_component.service.configuration import ServiceManagerConfig
from kaybee_component.service.manager import ServiceManager
from tests.unit.service.registry import ServiceRegistry


@pytest.fixture
def sm_config() -> ServiceManagerConfig:
    config = ServiceManagerConfig()
    return config


@pytest.fixture
def sm_registry():
    class TestServiceRegistry(ServiceRegistry):
        pass

    return TestServiceRegistry


@pytest.fixture
def sm(sm_config, sm_registry) -> ServiceManager:
    sm = ServiceManager(sm_config, sm_registry)
    return sm
