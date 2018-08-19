from dataclasses import dataclass, field
from typing import Type

import pytest

from kaybee_component.field_types import injected
from kaybee_component.service.base_service import BaseService
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


@pytest.fixture
def register_services(sm_registry):
    @sm_registry.service(name='view')
    @dataclass(frozen=True)
    class ViewService(BaseService):
        sm_config: ServiceManagerConfig = injected()

        @classmethod
        def register(cls):
            pass

    @sm_registry.service(name='request')
    @dataclass(frozen=True)
    class RequestService(BaseService):
        @classmethod
        def register(cls):
            pass


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
