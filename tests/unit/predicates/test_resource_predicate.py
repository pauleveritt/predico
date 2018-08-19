from dataclasses import dataclass

import dectate
import pytest
from dectate import ConflictError

from kaybee_component.predicates import ResourcePredicate
from kaybee_component.resource import Resource
from kaybee_component.viewtypes import IndexView


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


class TestResourcePredicate:
    def test_import(self):
        assert 'ResourcePredicate' == ResourcePredicate.__name__

    def test_construction(self):
        predicate = ResourcePredicate(value=Resource)
        assert 'resource' == predicate.key
        assert Resource == predicate.value
        assert 10 == predicate.rank

    def test_simple_registration(self, actions):
        assert 1 == len(actions)
        action, target = actions[0]
        assert 'for_-IndexView--resource-Resource' == action.name
        resource = action.predicates['resource']
        assert 'ResourcePredicate' == resource.__class__.__name__
        assert 20 == action.sort_order
        assert target.__name__.endswith('ResourceView')

    def test_str(self, first_action):
        resource = first_action.predicates['resource']
        assert 'resource-Resource' == str(resource)

    def test_matches(self, first_action):
        resource = first_action.predicates['resource']
        resource_class = resource.value
        assert resource.matches(resource_class)

    def test_not_matches(self, first_action):
        resource = first_action.predicates['resource']
        class OtherResource:
            pass

        assert not resource.matches(OtherResource)

    def test_conflict_error(self, committed_registry):
        @committed_registry.view(for_=IndexView, resource=Resource)
        @dataclass
        class ResourceView:
            logo: str = 'Logo XX'

        with pytest.raises(ConflictError):
            dectate.commit(committed_registry)
