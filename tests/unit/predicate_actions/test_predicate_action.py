from typing import Mapping, Union

import pytest

from predico.predicate_action import (
    PredicateAction, UnknownArgument,
    MissingArgument
)
from predico.predicates import ForPredicate, ResourcePredicate


class FakeIndexView:
    pass


class FakeResource:
    pass


class FakeViewAction(PredicateAction):
    action_name = 'view'
    REQUIRED_PREDICATES = (ForPredicate,)
    OPTIONAL_PREDICATES = (ResourcePredicate,)
    predicates: Mapping[str, Union[ForPredicate, ResourcePredicate]]


@pytest.fixture
def good_for_fva():
    fva = FakeViewAction(for_=FakeIndexView)
    return fva


@pytest.fixture
def good_resource_fva():
    fva = FakeViewAction(for_=FakeIndexView, resource=FakeResource)
    return fva


def test_required(good_for_fva):
    assert ['for_'] == list(good_for_fva.predicates.keys())
    assert 'for_-FakeIndexView' == good_for_fva.name
    assert 10 == good_for_fva.sort_order


def test_bad_required():
    with pytest.raises(UnknownArgument) as exc:
        FakeViewAction(xxxfor_=FakeIndexView)
    msg = str(exc.value)
    assert 'Decorator supplied unknown predicate: xxxfor_' == msg


def test_missing_required():
    with pytest.raises(MissingArgument) as exc:
        FakeViewAction()
    msg = str(exc.value)
    assert '__init__() missing 1 required positional argument: for_' == msg


def test_optional(good_resource_fva):
    good_for_fva = FakeViewAction(for_=FakeIndexView, resource=FakeResource)
    assert ['for_', 'resource'] == list(good_for_fva.predicates.keys())
    assert 'for_-FakeIndexView--resource-FakeResource' == good_for_fva.name
    assert 20 == good_for_fva.sort_order


def test_bad_optional():
    with pytest.raises(UnknownArgument) as exc:
        FakeViewAction(for_=FakeIndexView, xxxresource=FakeResource)
    msg = str(exc.value)
    assert 'Decorator supplied unknown predicate: xxxresource' == msg


def test_missing_required_with_optional():
    with pytest.raises(MissingArgument) as exc:
        FakeViewAction(resource=FakeResource)
    msg = str(exc.value)
    assert '__init__() missing 1 required positional argument: for_' == msg
