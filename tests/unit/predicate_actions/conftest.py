from dataclasses import dataclass
from typing import Mapping, Union

import dectate
import pytest

from kaybee_component.predicates import ForPredicate, ResourcePredicate
from kaybee_component.services.resource.base_resource import Resource
from kaybee_component.view import PredicateAction, ViewAction
from kaybee_component.viewtypes import IndexView


class NotView:
    pass


class NotResource:
    pass


@pytest.fixture
def registry():
    class ViewAction(PredicateAction):
        REQUIRED_PREDICATES = (ForPredicate,)
        OPTIONAL_PREDICATES = (ResourcePredicate,)
        predicates: Mapping[str, Union[ForPredicate, ResourcePredicate]]

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
