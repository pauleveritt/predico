"""

This is where the rubber meets the road on matching predicates.
Everything from the outside world filters through to here:

- request.get_view calls PredicateAction.get_class
- get_class sorts the actions and calls all_predicates_match
  to decide the first match
- all_predicates_match asks each predicate if it matches
- If not, it bails

"""
from dataclasses import dataclass, field
from typing import List

import pytest

from kaybee_component.predicate_action import predicates_match
from kaybee_component.predicates import (
    ForPredicate, ResourcePredicate,
    ResourceIdPredicate,
    ParentIdPredicate
)
from kaybee_component.services.request.base_request import Request
from kaybee_component.services.resource.base_resource import Resource


@dataclass
class FakeGoodResource(Resource):
    id: str = 'x/y/z'
    rtype: str = 'article'
    parentids: List[str] = field(default_factory=list)


@dataclass
class FakeBadResource(Resource):
    id: str = 'x/y/z'
    rtype: str = 'article'
    parentids: List[str] = field(default_factory=list)


@dataclass
class FakeRequest(Request):
    resource: Resource


@pytest.fixture
def fake_good_request():
    resource = FakeGoodResource(parentids=['x/y/index', 'x/index', 'index'])
    fr = FakeRequest(resource=resource)
    return fr


@pytest.fixture
def fake_bad_request():
    resource = FakeBadResource(parentids=['x/y/index', 'x/index', 'index'])
    fr = FakeRequest(resource=resource)
    return fr


class FakeGoodView:
    pass


class FakeBadView:
    pass


@pytest.fixture
def good_for_predicate():
    fp = ForPredicate(FakeGoodView)
    return fp


@pytest.fixture
def bad_for_predicate():
    fp = ForPredicate(FakeBadView)
    return fp


@pytest.fixture
def good_resource_predicate():
    rp = ResourcePredicate(FakeGoodResource)
    return rp


@pytest.fixture
def bad_resource_predicate():
    rp = ResourcePredicate(FakeBadResource)
    return rp


@pytest.fixture
def good_resourceid_predicate():
    rp = ResourceIdPredicate('x/y/z')
    return rp


@pytest.fixture
def bad_resourceid_predicate():
    rp = ResourceIdPredicate('1234')
    return rp


@pytest.fixture
def good_parentid_predicate():
    pp = ParentIdPredicate('x/index')
    return pp


@pytest.fixture
def bad_parentid_predicate():
    pp = ParentIdPredicate('bad/bad/bad/index')
    return pp


def test_match_empty_predicates_list(fake_good_request, good_for_predicate):
    result = predicates_match(fake_good_request, [])
    assert result


def test_match_for(fake_good_request, good_for_predicate):
    kwargs = dict(for_=FakeGoodView)
    predicate_values = [good_for_predicate]
    result = predicates_match(fake_good_request, predicate_values, **kwargs)
    assert result


def test_nomatch_for(fake_good_request, bad_for_predicate):
    """ View service asks for one view but registration is for another """
    kwargs = dict(for_=FakeGoodView)
    predicate_values = [bad_for_predicate]
    result = predicates_match(fake_good_request, predicate_values, **kwargs)
    assert not result


def test_match_resource(fake_good_request, good_resource_predicate):
    kwargs = dict(for_=FakeGoodView)
    predicate_values = [good_resource_predicate]
    result = predicates_match(fake_good_request, predicate_values, **kwargs)
    assert result


def test_nomatch_resource(fake_good_request, bad_resource_predicate):
    """ View service asks for one resource but registration is for another """
    kwargs = dict(for_=FakeGoodView)
    predicate_values = [bad_resource_predicate]
    result = predicates_match(fake_good_request, predicate_values, **kwargs)
    assert not result


def test_match_resourceid(fake_good_request, good_resourceid_predicate):
    kwargs = dict(for_=FakeGoodView)
    predicate_values = [good_resourceid_predicate]
    result = predicates_match(fake_good_request, predicate_values, **kwargs)
    assert result


def test_nomatch_resourceid(fake_good_request, bad_resourceid_predicate):
    kwargs = dict(for_=FakeGoodView)
    predicate_values = [bad_resourceid_predicate]
    result = predicates_match(fake_good_request, predicate_values, **kwargs)
    assert not result


def test_match_parentid(fake_good_request, good_parentid_predicate):
    kwargs = dict(for_=FakeGoodView)
    predicate_values = [good_parentid_predicate]
    result = predicates_match(fake_good_request, predicate_values, **kwargs)
    assert result


def test_nomatch_parentid(fake_good_request, bad_parentid_predicate):
    kwargs = dict(for_=FakeGoodView)
    predicate_values = [bad_parentid_predicate]
    result = predicates_match(fake_good_request, predicate_values, **kwargs)
    assert not result


# ---   Now some combinations

def test_good_for_good_resource(fake_good_request, good_for_predicate,
                                good_resource_predicate):
    kwargs = dict(for_=FakeGoodView)
    predicate_values = [good_for_predicate, good_resource_predicate]
    result = predicates_match(fake_good_request, predicate_values,
                              **kwargs)
    assert result


def test_good_for_bad_resource(fake_good_request, good_for_predicate,
                               bad_resource_predicate):
    kwargs = dict(for_=FakeGoodView)
    predicate_values = [good_for_predicate, bad_resource_predicate]
    result = predicates_match(fake_good_request, predicate_values,
                              **kwargs)
    assert not result
