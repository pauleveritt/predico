from dataclasses import dataclass
from typing import Mapping, Union

import dectate
import pytest

from predico.predicate_action import PredicateAction
from predico.predicates import ForPredicate, ResourcePredicate


class FakeResource:
    pass


class FakeIndexView:
    pass


@dataclass
class FakeForView:
    name: str = 'Fake For View'


@dataclass
class FakeResourceView:
    name: str = 'Fake Resource View'


class FakeViewAction(PredicateAction):
    action_name = 'view'
    REQUIRED_PREDICATES = (ForPredicate,)
    OPTIONAL_PREDICATES = (ResourcePredicate,)
    predicates: Mapping[str, Union[ForPredicate, ResourcePredicate]]


@pytest.fixture
def uncommitted_registry():
    class FakePredicateApp(dectate.App):
        view = dectate.directive(FakeViewAction)

    return FakePredicateApp


@pytest.fixture
def for_view(uncommitted_registry):
    uncommitted_registry.view(for_=FakeIndexView)(FakeForView)


@pytest.fixture
def resource_view(uncommitted_registry):
    uncommitted_registry.view(for_=FakeIndexView, resource=FakeResource)(
        FakeResourceView)


@pytest.fixture
def committed_registry(uncommitted_registry, for_view, resource_view):
    dectate.commit(uncommitted_registry)
    return uncommitted_registry


@pytest.fixture
def actions(committed_registry):
    q = dectate.Query('view')
    actions = list(q(committed_registry))
    return actions


@pytest.fixture
def sorted_actions(committed_registry):
    sa = FakeViewAction.sorted_actions(committed_registry)
    return sa


@pytest.fixture
def forview_action(actions) -> FakeViewAction:
    return actions[0][0]


def test_sorted_both(sorted_actions):
    assert FakeResourceView == sorted_actions[0][1]
    assert FakeForView == sorted_actions[1][1]
