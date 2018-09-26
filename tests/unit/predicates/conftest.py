from dataclasses import dataclass

import dectate
import pytest

from kaybee_component.services.resource.base_resource import Resource
from kaybee_component.services.view.action import ViewAction


class TestIndexView:
    pass


@dataclass
class TestForView:
    title: str = 'Test For View'


@dataclass
class TestResourceView:
    title: str = 'Resource View'


@dataclass
class TestParentSelfView:
    title: str = 'Test ParentSelf View'


@dataclass
class TestConflictView:
    title: str = 'Conflicts with TestResourceView'


@pytest.fixture
def registry():
    class PredicateApp(dectate.App):
        view = dectate.directive(ViewAction)

    return PredicateApp


@pytest.fixture
def for_view(registry):
    registry.view(for_=TestIndexView)(TestForView)

    dectate.commit(registry)


@pytest.fixture
def resource_view(registry):
    registry.view(for_=TestIndexView, resource=Resource)(TestResourceView)

    dectate.commit(registry)


@pytest.fixture
def parentself_view(registry):
    registry.view(for_=TestIndexView, parentself='more/about')(
        TestParentSelfView)

    dectate.commit(registry)


@pytest.fixture
def generate_conflict_for(registry, resource_view):
    def conflict():
        registry.view(for_=TestIndexView)(TestResourceView)
        registry.view(for_=TestIndexView)(TestParentSelfView)
        dectate.commit(registry)

    return conflict


@pytest.fixture
def generate_conflict_resource(registry, resource_view):
    def conflict():
        registry.view(for_=TestIndexView, resource=Resource)(
            TestParentSelfView)
        dectate.commit(registry)

    return conflict


@pytest.fixture
def request(registry):
    class Resource:
        pass

    class Request:
        pass

    r = Request()
    resource1 = Resource()
    resource1.parentids = ['more/about']

    r.resourceid = 'a/b/c/d/e'
    r.registry = registry
    r.resource = resource1
    return r
