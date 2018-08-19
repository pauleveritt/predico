from dataclasses import dataclass

import dectate
import pytest

from kaybee_component.resource import Resource
from kaybee_component.view import ViewAction
from kaybee_component.viewtypes import IndexView


@pytest.fixture
def registry():
    class PredicateApp(dectate.App):
        view = dectate.directive(ViewAction)

    return PredicateApp


@pytest.fixture
def for_view(registry):
    @registry.view(for_=IndexView)
    @dataclass
    class ForView:
        logo: str = 'Logo XX'

    dectate.commit(registry)


@pytest.fixture
def resource_view(registry):
    @registry.view(for_=IndexView, resource=Resource)
    @dataclass
    class ResourceView:
        logo: str = 'Logo XX'

    dectate.commit(registry)


@pytest.fixture
def committed_registry(registry, for_view, resource_view):
    dectate.commit(registry)
    return registry


@pytest.fixture
def actions(committed_registry):
    q = dectate.Query('view')
    actions = list(q(committed_registry))
    return actions


@pytest.fixture
def forview_action(actions) -> ViewAction:
    return actions[0][0]


@pytest.fixture
def resourceview_action(actions) -> ViewAction:
    return actions[1][0]
