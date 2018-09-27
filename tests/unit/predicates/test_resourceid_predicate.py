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
