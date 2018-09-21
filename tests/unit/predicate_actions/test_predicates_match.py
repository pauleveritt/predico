import pytest

from kaybee_component.predicate_action import (
    LookupMissingRequired,
    UnknownLookup
)
from kaybee_component.services.resource.base_resource import Resource
from kaybee_component.services.view.action import ViewAction
from kaybee_component.services.view.base_view import IndexView
from tests.unit.predicate_actions.conftest import NotView, NotResource


def test_missing_argument(forview_action):
    with pytest.raises(LookupMissingRequired) as exc:
        forview_action.all_predicates_match(resource=999)
    m = 'Lookup is missing required field: for_'
    assert str(exc.value).startswith(m)


def test_unknown_argument(forview_action):
    with pytest.raises(UnknownLookup) as exc:
        forview_action.all_predicates_match(for_=IndexView, bogus=999)
    m = 'Lookup supplied unknown predicate argument: bogus'
    assert str(exc.value).startswith(m)


def test_predicates_for_match(forview_action: ViewAction):
    assert True is forview_action.all_predicates_match(for_=IndexView)


def test_predicates_for_not_match(forview_action: ViewAction):
    assert False is forview_action.all_predicates_match(for_=NotView)


def test_predicates_resource_match(resourceview_action: ViewAction):
    assert True is resourceview_action.all_predicates_match(
        for_=IndexView,
        resource=Resource
    )


def test_predicates_resource_not_match(resourceview_action: ViewAction):
    assert False is resourceview_action.all_predicates_match(
        for_=IndexView,
        resource=NotResource
    )


def test_predicates_resource_not_for__match(resourceview_action: ViewAction):
    assert False is resourceview_action.all_predicates_match(
        for_=NotView,
        resource=Resource
    )


def test_resourceview_action_not_handed_resource(resourceview_action):
    assert False is resourceview_action.all_predicates_match(
        for_=IndexView)
