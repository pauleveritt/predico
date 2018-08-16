from dataclasses import dataclass

import dectate
import pytest

from kaybee_component.resources import Resource
from kaybee_component.views import ViewAction
from kaybee_component.viewtypes import IndexView


@dataclass
class ForView:
    logo: str = 'Logo XX'


@pytest.fixture
def registry():
    class PredicateApp(dectate.App):
        view = dectate.directive(ViewAction)

    return PredicateApp


@pytest.fixture
def for_view(registry):
    @registry.view(for_=IndexView)
    @dataclass
    class ForView:
        logo: str = 'Logo XX'

    dectate.commit(registry)


@pytest.fixture
def resource_view(registry):
    @registry.view(for_=IndexView, resource=Resource)
    @dataclass
    class ResourceView:
        logo: str = 'Logo XX'

    dectate.commit(registry)

# @pytest.fixture
# def two_predicate_view(registry):
#     return
#
#     @registry.view(for_=IndexView)
#     @dataclass
#     class ArticleView:
#         logo: str = 'Logo XX'
