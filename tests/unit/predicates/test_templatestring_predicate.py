import pytest

from predico.predicates import TemplateStringPredicate
from predico.services.request.base_request import Request


@pytest.fixture
def templatestring_predicate():
    ts = TemplateStringPredicate('<p>Some Template</p>')
    return ts


def test_construction(templatestring_predicate):
    assert '<p>Some Template</p>' == templatestring_predicate.value
    assert 'template_string' == templatestring_predicate.key


def test_str(templatestring_predicate):
    assert 'template_string' == str(templatestring_predicate)


def test_matches(templatestring_predicate):
    request = Request()
    with pytest.raises(NotImplementedError):
        assert templatestring_predicate.matches(request)
