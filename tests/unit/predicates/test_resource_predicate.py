from dataclasses import dataclass

import pytest

from kaybee_component.predicates import ResourcePredicate
from kaybee_component.services.resource.base_resource import Resource


@dataclass
class FakeResource(Resource):
    pass


@dataclass
class FakeRequest:
    resource: FakeResource


@pytest.fixture
def test_resource():
    resource = FakeResource(rtype='FakeResource', id='more/about')
    return resource


@pytest.fixture
def test_request(test_resource):
    tr = FakeRequest(resource=test_resource)
    return tr


@pytest.fixture
def resource_predicate():
    pp = ResourcePredicate(FakeResource)
    return pp


@pytest.fixture
def notmatches_resource_predicate():
    class BadResource:
        pass
    pp = ResourcePredicate(BadResource)
    return pp


def test_construction(resource_predicate):
    assert FakeResource == resource_predicate.value
    assert 'resource' == resource_predicate.key
    assert 10 == resource_predicate.rank


def test_str(resource_predicate):
    assert 'resource-FakeResource' == str(resource_predicate)


def test_matches(resource_predicate, test_request):
    assert resource_predicate.matches(test_request)


def test_not_matches(notmatches_resource_predicate, test_request):
    assert not notmatches_resource_predicate.matches(test_request)

# import dectate
# import pytest
# from dectate import ConflictError
# 
# from kaybee_component.predicates import ParentSelfPredicate
# 
# 
# @pytest.fixture
# def committed_registry(registry, resource_view):
#     dectate.commit(registry)
#     return registry
# 
# 
# @pytest.fixture
# def actions(committed_registry):
#     q = dectate.Query('view')
#     actions = list(q(committed_registry))
#     return actions
# 
# 
# @pytest.fixture
# def first_action(actions):
#     return actions[0][0]
# 
# 
# def test_construction():
#     predicate = ParentSelfPredicate(value='more/about', action=None)
#     assert 'parentself' == predicate.key
#     assert 'more/about' == predicate.value
#     assert 20 == predicate.rank
# 
# 
# def test_simple_registration(actions):
#     assert 1 == len(actions)
#     action, target = actions[0]
#     assert 'for_-TestIndexView--resource-Resource' == action.name
#     resource = action.predicates['resource']
#     assert 'ResourcePredicate' == resource.__class__.__name__
#     assert 20 == action.sort_order
#     assert target.__name__.endswith('ResourceView')
# 
# 
# def test_str(first_action):
#     resource = first_action.predicates['resource']
#     assert 'resource-Resource' == str(resource)
# 
# 
# def test_matches(first_action):
#     resource = first_action.predicates['resource']
#     resource_class = resource.value
#     assert resource.matches(resource_class)
# 
# 
# def test_not_matches(first_action):
#     resource = first_action.predicates['resource']
# 
#     class OtherResource:
#         pass
# 
#     assert not resource.matches(OtherResource)
# 
# 
# def test_conflict_error(generate_conflict_resource):
#     with pytest.raises(ConflictError):
#         generate_conflict_resource()
