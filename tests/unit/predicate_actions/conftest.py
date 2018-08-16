from dataclasses import dataclass
from typing import Mapping, Union

import dectate
import pytest

from kaybee_component.predicates import ForPredicate, ResourcePredicate
from kaybee_component.resources import Resource
from kaybee_component.views import PredicateAction
from kaybee_component.viewtypes import IndexView


@pytest.fixture
def registry():
    class ViewAction(PredicateAction):
        REQUIRED_PREDICATES = (ForPredicate,)
        OPTIONAL_PREDICATES = (ResourcePredicate,)
        predicates: Mapping[str, Union[ForPredicate, ResourcePredicate]]

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

