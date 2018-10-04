from dataclasses import dataclass
from typing import List

import pytest

from predico.predicates import ResourceIdPredicate
from predico.services.resource.base_resource import Resource


@dataclass
class FakeResource(Resource):
    pass


@dataclass
class AnotherFakeResource(Resource):
    pass


@pytest.fixture
def another_resource():
    resource = AnotherFakeResource(id='more/another', rtype='fakeresource')
    return resource


@dataclass
class FakeRequest:
    resource: FakeResource


@pytest.fixture
def test_resource():
    resource = FakeResource(id='more/about', rtype='fakeresource')
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
def another_resourceid_predicate():
    pp = ResourceIdPredicate('more/another')
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


def test_matches_args(another_resourceid_predicate, test_request,
                      another_resource):
    """ Do not use resource from the request and still match """
    assert another_resourceid_predicate.matches(
        test_request,
        resource=another_resource,
    )


def test_not_matches_args(resourceid_predicate, test_request,
                          another_resource):
    """ Do not use resource from the request and not match """
    assert not resourceid_predicate.matches(
        test_request,
        resource=another_resource,
    )
