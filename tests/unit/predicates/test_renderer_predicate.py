import pytest

from predico.predicates import RendererPredicate
from predico.services.request.base_request import Request


class FakeStringFormatRenderer:
    pass


@pytest.fixture
def renderer_predicate():
    rp = RendererPredicate(FakeStringFormatRenderer)
    return rp


def test_construction(renderer_predicate):
    assert FakeStringFormatRenderer == renderer_predicate.value
    assert 'renderer' == renderer_predicate.key


def test_str(renderer_predicate):
    assert 'renderer' == str(renderer_predicate)


def test_matches(renderer_predicate):
    request = Request()
    with pytest.raises(NotImplementedError):
        assert renderer_predicate.matches(request)
