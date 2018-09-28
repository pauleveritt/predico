from dataclasses import dataclass
from typing import Type

import pytest

from predico.registry import Registry
from predico.servicemanager.base_service import BaseService
from predico.servicemanager.manager import ServiceManager


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
