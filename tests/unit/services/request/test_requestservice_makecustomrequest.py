from dataclasses import dataclass
from typing import Optional

import pytest

from predico.services.request.common_request import CommonRequest
from predico.services.request.config import RequestServiceConfig


@dataclass(frozen=True)
class FakeSphinxRequest(CommonRequest):
    """ Custom request to test factory and also passing props """

    prev: Optional[str] = None
    next: Optional[str] = None


@pytest.fixture
def requestservice_config() -> RequestServiceConfig:
    """ Have these tests use a config with different factory """

    config = RequestServiceConfig(
        flag=23,
        factory=FakeSphinxRequest,
    )
    return config


def test_custom_request_factory(requestservice, requestservice_config):
    assert 23 == requestservice_config.flag
    assert FakeSphinxRequest == requestservice.config.factory


def test_make_custom_request(requestservice):
    request: FakeSphinxRequest = requestservice.make_request('more/about')
    assert FakeSphinxRequest == request.__class__
    assert None is request.prev
    assert None is request.next


def test_make_custom_request_props(requestservice):
    request: FakeSphinxRequest = requestservice.make_request(
        'more/about',
        prev='Previous',
        next='Next',
    )
    assert FakeSphinxRequest == request.__class__
    assert 'Previous' is request.prev
    assert 'Next' is request.next
