"""

Test various combinations of view matching via the request.

"""
from dataclasses import dataclass

import dectate
import pytest

from kaybee_component.services.resource.base_resource import Resource


@dataclass
class TestArticle(Resource):
    title: str


@pytest.fixture
def test_article(test_registry):
    test_registry.resource('article')(TestArticle)


@pytest.fixture
def registrations(test_registry, test_article):
    dectate.commit(test_registry)
