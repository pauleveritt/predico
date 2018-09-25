import dectate
import pytest
from dectate import ConflictError

from kaybee_component.predicates import ResourcePredicate
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


@pytest.fixture
def parentself(first_action):
    return first_action.predicates['parentself']


def test_construction():
    predicate = ResourcePredicate(value=Resource, action=None)
    assert 'resource' == predicate.key
    assert Resource == predicate.value
    assert 10 == predicate.rank


def test_simple_registration(actions, parentself):
    assert 1 == len(actions)
    action, target = actions[0]
    assert 'for_-TestIndexView--parentself-more/about' == action.name
    assert 'ParentSelfPredicate' == parentself.__class__.__name__
    assert 30 == action.sort_order
    assert target.__name__.endswith('TestParentSelfView')


def test_str(first_action, parentself):
    assert 'parentself-more/about' == str(parentself)


def test_matches(first_action, parentself, request):
    parentself_value = parentself.value
    assert parentself.matches(parentself_value, request)


def test_match_self(first_action, parentself, request):
    assert not parentself.matches('another/place', request)


def test_match_parent(first_action, parentself, request):
    assert not parentself.matches('another/place', request)


def test_match_grandparent(first_action, parentself, request):
    assert not parentself.matches('another/place', request)


def test_no_match(first_action, parentself, request):
    assert not parentself.matches('another/place', request)


def test_conflict_error(generate_conflict_resource):
    with pytest.raises(ConflictError):
        generate_conflict_resource()
