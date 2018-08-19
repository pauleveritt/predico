from dataclasses import dataclass, field
from typing import Type, Sequence, Any

import pytest

from kaybee_component.field_types import injected, injectedattr
from kaybee_component.service.base_service import BaseService
from kaybee_component.service.configuration import ServiceManagerConfig
from kaybee_component.service.manager import ServiceManager
from kaybee_component.services.view.config import ViewServiceConfig
from kaybee_component.service.registry import ServiceRegistry


@pytest.fixture
def viewservice_config() -> ViewServiceConfig:
    config = ViewServiceConfig(flag=99)
    return config


@pytest.fixture
def sm_config(viewservice_config) -> ServiceManagerConfig:
    config = ServiceManagerConfig(
        serviceconfigs=dict(
            viewservice=viewservice_config,
        )
    )
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
        config: ViewServiceConfig = injected()
        allconfigs: Sequence[Any] = injectedattr(ServiceManagerConfig,
                                                 'serviceconfigs')

        @classmethod
        def register(cls):
            pass

    @sm_registry.service(name='request')
    @dataclass(frozen=True)
    class RequestService(BaseService):
        sm_config: ServiceManagerConfig = injected()

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
