import dectate
import pytest
from dectate import ConflictError

from kaybee_component.predicates import ParentSelfPredicate


@pytest.fixture
def committed_registry(registry, resource_view):
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
    predicate = ParentSelfPredicate(value='more/about', action=None)
    assert 'parentself' == predicate.key
    assert 'more/about' == predicate.value
    assert 20 == predicate.rank


def test_simple_registration(actions):
    assert 1 == len(actions)
    action, target = actions[0]
    assert 'for_-TestIndexView--resource-Resource' == action.name
    resource = action.predicates['resource']
    assert 'ResourcePredicate' == resource.__class__.__name__
    assert 20 == action.sort_order
    assert target.__name__.endswith('ResourceView')


def test_str(first_action):
    resource = first_action.predicates['resource']
    assert 'resource-Resource' == str(resource)


def test_matches(first_action):
    resource = first_action.predicates['resource']
    resource_class = resource.value
    assert resource.matches(resource_class)


def test_not_matches(first_action):
    resource = first_action.predicates['resource']

    class OtherResource:
        pass

    assert not resource.matches(OtherResource)


def test_conflict_error(generate_conflict_resource):
    with pytest.raises(ConflictError):
        generate_conflict_resource()
