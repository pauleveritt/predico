from dataclasses import dataclass
from typing import List

import pytest

from predico.predicates import ParentIdPredicate
from predico.services.resource.base_resource import Resource


@dataclass
class FakeResource(Resource):
    parentids: List[str]


@dataclass
class AnotherFakeResource(Resource):
    parentids: List[str]


@dataclass
class FakeRequest:
    resource: FakeResource


@pytest.fixture
def fake_resource():
    resource = FakeResource(
        parentids=['more/index', 'index'],
        id='more/about',
        rtype='fakeresource'
    )
    return resource


@pytest.fixture
def another_resource():
    resource = FakeResource(
        parentids=['another/index', 'index'],
        id='another/more',
        rtype='fakeresource'
    )
    return resource


@pytest.fixture
def test_request(fake_resource):
    tr = FakeRequest(resource=fake_resource)
    return tr


@pytest.fixture
def parentid_predicate():
    pp = ParentIdPredicate('more/index')
    return pp


@pytest.fixture
def another_parentid_predicate():
    pp = ParentIdPredicate('another/index')
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


def test_matches_args(another_parentid_predicate, test_request,
                      another_resource):
    """ Do not use resource from the request and still match """
    assert another_parentid_predicate.matches(
        test_request,
        resource=another_resource,
    )


def test_not_matches_args(parentid_predicate, test_request,
                      another_resource):
    """ Do not use resource from the request and not match """
    assert not parentid_predicate.matches(
        test_request,
        resource=another_resource,
    )
