from dataclasses import dataclass

import pytest

from kaybee_component.field_types import injected
from kaybee_component.services.request.registry import BaseRequestRegistry
from kaybee_component.services.request.config import RequestServiceConfig
from kaybee_component.services.request.service import RequestService


@pytest.fixture
def rs_config() -> RequestServiceConfig:
    config = RequestServiceConfig(flag=99)
    return config


@pytest.fixture
def rs_registry():
    class TestRequestServiceRegistry(BaseRequestRegistry):
        pass

    return TestRequestServiceRegistry


@pytest.fixture
def rs(rs_config, rs_registry) -> RequestService:
    service = RequestService(rs_registry, rs_config)
    return service


@pytest.fixture
def register_services(rs_registry):
    @rs_registry.request(name='request')
    @dataclass(frozen=True)
    class SphinxRequest(BaseService):
        config: RequestServiceConfig = injected()

        @classmethod
        def register(cls):
            pass


@pytest.fixture
def initialized_rs(rs):
    rs.initialize()
    return rs
