from dataclasses import dataclass

import dectate
import pytest
from dectate import ConflictError

from kaybee_component.predicates import ParentSelfPredicate
from kaybee_component.services.resource.base_resource import Resource


@pytest.fixture
def committed_registry(registry, parentself_view):
    dectate.commit(registry)
    return registry


@pytest.fixture
def actions(committed_registry):
    q = dectate.Query('view')
    actions = list(q(committed_registry))
    return actions


@pytest.fixture
def first_action(actions):
    return actions[0][0]


def test_construction():
    predicate = ParentSelfPredicate(value=Resource, action=None)
    assert 'parentself' == predicate.key
    assert Resource == predicate.value
    assert 20 == predicate.rank


def test_simple_registration(actions):
    assert 1 == len(actions)
    action, target = actions[0]
    assert 'for_-TestIndexView--parentself-Resource' == action.name
    parentself = action.predicates['parentself']
    assert 'ParentSelfPredicate' == parentself.__class__.__name__
    assert 30 == action.sort_order
    assert target.__name__.endswith('ResourceView')


def test_str(first_action):
    parentself = first_action.predicates['parentself']
    assert 'parentself-Resource' == str(parentself)


def test_matches(first_action):
    parentself = first_action.predicates['parentself']
    resource_class = parentself.value
    assert parentself.matches(resource_class)


def test_not_matches(first_action):
    parentself = first_action.predicates['parentself']

    class OtherResource:
        pass

    assert not parentself.matches(OtherResource)


def test_conflict_error(committed_registry, testindexview):
    @committed_registry.view(for_=testindexview, resource=Resource)
    @dataclass
    class ResourceView:
        logo: str = 'Logo XX'

    with pytest.raises(ConflictError):
        dectate.commit(committed_registry)
