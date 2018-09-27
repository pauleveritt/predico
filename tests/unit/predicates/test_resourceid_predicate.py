from dataclasses import dataclass
from typing import List

import pytest

from kaybee_component.predicates import ResourceIdPredicate


@dataclass
class FakeResource:
    parentids: List[str]
    id: str


@dataclass
class FakeRequest:
    resource: FakeResource


@pytest.fixture
def test_resource():
    resource = FakeResource(
        parentids=['more/index', 'index'],
        id='more/about'
    )
    return resource


@pytest.fixture
def test_request(test_resource):
    tr = FakeRequest(resource=test_resource)
    return tr


@pytest.fixture
def resourceid_predicate():
    pp = ResourceIdPredicate('more/about')
    return pp


@pytest.fixture
def notmatches_resourceid_predicate():
    pp = ResourceIdPredicate('xxx/yyy/zzz')
    return pp


def test_construction(resourceid_predicate):
    assert 'more/about' == resourceid_predicate.value
    assert 'resourceid' == resourceid_predicate.key
    assert 30 == resourceid_predicate.rank


def test_str(resourceid_predicate):
    assert 'resourceid-more/about' == str(resourceid_predicate)


def test_matches(resourceid_predicate, test_request):
    assert resourceid_predicate.matches(test_request)


def test_not_matches(notmatches_resourceid_predicate, test_request):
    assert not notmatches_resourceid_predicate.matches(test_request)

# import dectate
# import pytest
# from dectate import ConflictError
#
# from kaybee_component.predicates import ResourcePredicate
# from kaybee_component.services.resource.base_resource import Resource
#
#
# @pytest.fixture
# def committed_registry(registry, parentself_view):
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
# @pytest.fixture
# def parentself(first_action):
#     return first_action.predicates['parentself']
#
#
# def test_construction():
#     predicate = ResourcePredicate(value=Resource, action=None)
#     assert 'resource' == predicate.key
#     assert Resource == predicate.value
#     assert 10 == predicate.rank
#
#
# def test_simple_registration(actions, parentself):
#     assert 1 == len(actions)
#     action, target = actions[0]
#     assert 'for_-TestIndexView--parentself-more/about' == action.name
#     assert 'ParentSelfPredicate' == parentself.__class__.__name__
#     assert 30 == action.sort_order
#     assert target.__name__.endswith('TestParentSelfView')
#
#
# def test_str(first_action, parentself):
#     assert 'parentself-more/about' == str(parentself)
#
#
# def test_matches(first_action, parentself, request):
#     parentself_value = parentself.value
#     assert parentself.matches(parentself_value, request)
#
#
# # def test_match_self(first_action, parentself, request):
# #     assert not parentself.matches('another/place', request)
# #
# #
# # def test_match_parent(first_action, parentself, request):
# #     assert not parentself.matches('another/place', request)
# #
# #
# # def test_match_grandparent(first_action, parentself, request):
# #     assert not parentself.matches('another/place', request)
# #
# #
# # def test_no_match(first_action, parentself, request):
# #     assert not parentself.matches('another/place', request)
#
#
# def test_conflict_error(generate_conflict_resource):
#     with pytest.raises(ConflictError):
#         generate_conflict_resource()
