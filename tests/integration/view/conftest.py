"""

Test various combinations of view matching via the request.

"""
from dataclasses import dataclass

import dectate
import pytest

from kaybee_component.services.view.base_view import IndexView
from kaybee_component.services.view.config import ViewServiceConfig


@dataclass
class TestResourceView:
    viewservice_config: ViewServiceConfig
    name: str = 'Generic Resource View'


@dataclass
class TestSectionView:
    viewservice_config: ViewServiceConfig
    name: str = 'Section View'

@dataclass
class TestResourceIdView:
    viewservice_config: ViewServiceConfig
    name: str = 'One Specific Resource ID'


@pytest.fixture
def register_views(test_registry, testarticle_class):
    test_registry.view(for_=IndexView)(TestResourceView)
    test_registry.view(for_=IndexView, resource=testarticle_class)(
        TestSectionView)
    # test_registry.view(for_=IndexView,
    #                    resource=testarticle_class,
    #                    resourceid='more/specificid'
    #                    )(TestResourceIdView)


@pytest.fixture
def registrations(test_registry, register_views, test_article, test_section):
    dectate.commit(test_registry)
