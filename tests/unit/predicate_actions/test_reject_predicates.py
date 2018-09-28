from dataclasses import dataclass, field
from typing import List

import pytest

from predico.predicate_action import (
    reject_predicates, UnknownLookup,
    LookupMissingRequired
)
from predico.predicates import ForPredicate, ResourcePredicate
from predico.services.resource.base_resource import Resource


class FakeGoodView:
    pass


@dataclass
class FakeGoodResource(Resource):
    id: str = 'x/y/z'
    rtype: str = 'article'
    parentids: List[str] = field(default_factory=list)


@pytest.fixture
def good_for_predicate():
    fp = ForPredicate(FakeGoodView)
    return fp


@pytest.fixture
def good_resource_predicate():
    rp = ResourcePredicate(FakeGoodResource)
    return rp


def test_good_none():
    required = []
    optional = []
    kwargs = dict()
    assert None is reject_predicates(required, optional, **kwargs)


def test_good_for(good_for_predicate):
    required = [good_for_predicate]
    optional = []
    kwargs = dict(for_=FakeGoodView)
    assert None is reject_predicates(required, optional, **kwargs)


def test_unknown_lookup():
    required = []
    optional = []
    kwargs = dict(for_=FakeGoodView)
    with pytest.raises(UnknownLookup) as exc:
        reject_predicates(required, optional, **kwargs)
    msg = 'Lookup supplied unknown predicate argument: for_'
    assert msg == str(exc.value)


def test_lookup_missing_required(good_for_predicate):
    required = [good_for_predicate]
    optional = []
    kwargs = dict()
    with pytest.raises(LookupMissingRequired) as exc:
        reject_predicates(required, optional, **kwargs)
    msg = 'Lookup is missing required field: for_'
    assert msg == str(exc.value)


def test_unknown_lookup_with_optional(good_resource_predicate):
    required = []
    optional = [good_resource_predicate]
    kwargs = dict(for_=FakeGoodView)
    with pytest.raises(UnknownLookup) as exc:
        reject_predicates(required, optional, **kwargs)
    msg = 'Lookup supplied unknown predicate argument: for_'
    assert msg == str(exc.value)


def test_lookup_missing_required_with_optional(good_for_predicate,
                                               good_resource_predicate):
    required = [good_for_predicate]
    optional = [good_resource_predicate]
    kwargs = dict()
    with pytest.raises(LookupMissingRequired) as exc:
        reject_predicates(required, optional, **kwargs)
    msg = 'Lookup is missing required field: for_'
    assert msg == str(exc.value)
