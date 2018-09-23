from dataclasses import dataclass

import dectate
import pytest

from kaybee_component.services.resource.base_resource import Resource
from kaybee_component.services.view.action import ViewAction


class TestIndexView:
    pass


@pytest.fixture
def testindexview():
    # Use a fixture so that equality test works. pytest puts the
    # import at a different place so it wrongly fails equality match.

    return TestIndexView


@pytest.fixture
def registry():
    class PredicateApp(dectate.App):
        view = dectate.directive(ViewAction)

    return PredicateApp


@pytest.fixture
def for_view(registry, testindexview):
    @registry.view(for_=testindexview)
    @dataclass
    class ForView:
        logo: str = 'Logo XX'

    dectate.commit(registry)


@pytest.fixture
def resource_view(registry, testindexview):
    @registry.view(for_=testindexview, resource=Resource)
    @dataclass
    class ResourceView:
        logo: str = 'Logo XX'

    dectate.commit(registry)
