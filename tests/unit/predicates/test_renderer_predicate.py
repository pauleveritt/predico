import pytest

from predico.predicates import RendererPredicate
from predico.services.request.base_request import Request


class StringFormatRenderer:
    pass


@pytest.fixture
def renderer_predicate():
    rp = RendererPredicate(StringFormatRenderer)
    return rp


def test_construction(renderer_predicate):
    assert StringFormatRenderer == renderer_predicate.value
    assert 'renderer' == renderer_predicate.key


def test_str(renderer_predicate):
    assert 'renderer' == str(renderer_predicate)


def test_matches(renderer_predicate):
    request = Request()
    with pytest.raises(NotImplementedError):
        assert renderer_predicate.matches(request)
