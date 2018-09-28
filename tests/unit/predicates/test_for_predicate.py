import pytest

from predico.predicates import ForPredicate
from predico.services.request.base_request import Request


class FakeRequest(Request):
    pass


@pytest.fixture
def test_request():
    tr = FakeRequest()
    return tr


class TestIndexView:
    pass


@pytest.fixture
def for_predicate():
    fp = ForPredicate(TestIndexView)
    return fp


def test_construction(for_predicate):
    assert TestIndexView == for_predicate.value
    assert 'for_' == for_predicate.key
    assert 10 == for_predicate.rank


def test_str(for_predicate):
    assert 'for_-TestIndexView' == str(for_predicate)


def test_matches(for_predicate, test_request):
    assert for_predicate.matches(test_request, for_=TestIndexView)


def test_not_matches(for_predicate, test_request):
    class BadView:
        pass

    assert not for_predicate.matches(test_request, for_=BadView)
