from dataclasses import dataclass

import pytest

from predico.predicates import ResourcePredicate
from predico.services.resource.base_resource import Resource


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
