"""

Test various combinations of view matching via the request.

"""
from dataclasses import dataclass

import dectate
import pytest

from kaybee_component.service.manager import Services
from kaybee_component.services.view.base_view import IndexView
from kaybee_component.services.view.config import ViewServiceConfig


@dataclass
class ForView1:
    viewservice_config: ViewServiceConfig
    name: str = 'For View One'


@pytest.fixture
def for_view1(test_registry):
    test_registry.view(for_=IndexView)(ForView1)


@pytest.fixture
def registrations(test_registry, for_view1):
    dectate.commit(test_registry)


@pytest.fixture
def services(initialized_sm) -> Services:
    services: Services = initialized_sm.services
    return services
