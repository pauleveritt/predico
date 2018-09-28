from dataclasses import dataclass
from typing import List

import pytest

from predico.predicates import ParentIdPredicate


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
def parentid_predicate():
    pp = ParentIdPredicate('more/index')
    return pp


@pytest.fixture
def notmatches_parentid_predicate():
    pp = ParentIdPredicate('xxx/yyy/zzz')
    return pp


def test_construction(parentid_predicate):
    assert 'more/index' == parentid_predicate.value
    assert 'parentid' == parentid_predicate.key
    assert 20 == parentid_predicate.rank


def test_str(parentid_predicate):
    assert 'parentid-more/index' == str(parentid_predicate)


def test_matches(parentid_predicate, test_request):
    assert parentid_predicate.matches(test_request)


def test_not_matches(notmatches_parentid_predicate, test_request):
    assert not notmatches_parentid_predicate.matches(test_request)
