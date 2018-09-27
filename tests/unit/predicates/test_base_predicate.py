import pytest

from kaybee_component.predicates import Predicate
from kaybee_component.services.request.base_request import Request


class TestIndexView:
    pass


@pytest.fixture
def base_predicate_value_string():
    bp = Predicate('more/about', 'base')
    return bp


@pytest.fixture
def base_predicate_value_class():
    """ The value argument is a class, not a string """

    # This triggers the branch in the __str__
    bp = Predicate(TestIndexView, 'base')
    return bp


def test_construction(base_predicate_value_string):
    assert 'more/about' == base_predicate_value_string.value
    assert 'base' == base_predicate_value_string.key
    assert 10 == base_predicate_value_string.rank


def test_value_str(base_predicate_value_string):
    assert 'base-more/about' == str(base_predicate_value_string)


def test_value_class(base_predicate_value_class):
    assert 'base-TestIndexView' == str(base_predicate_value_class)


def test_matches_not_implemented(base_predicate_value_string):
    class FakeRequest(Request):
        pass

    tr = FakeRequest()
    with pytest.raises(NotImplementedError):
        base_predicate_value_string.matches(tr, for_=TestIndexView)
