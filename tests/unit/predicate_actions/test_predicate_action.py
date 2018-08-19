from dataclasses import dataclass

import dectate
import pytest

from kaybee_component.predicate_action import (
    UnknownArgument, MissingArgument,
    LookupMissingRequired,
    UnknownLookup
)
from kaybee_component.services.resource.base_resource import Resource
from kaybee_component.services.view.action import ViewAction
from kaybee_component.services.view.base_view import IndexView
from tests.unit.predicate_actions.conftest import NotView, NotResource


class TestViewAction:
    def test_import(self, actions):
        assert 'ViewAction' == ViewAction.__name__

    def test_construction(self, actions):
        assert 2 == len(actions)

    def test_missing_for(self, registry):
        @registry.view()
        @dataclass
        class ForView:
            logo: str = 'Logo XX'

        with pytest.raises(MissingArgument) as exc:
            dectate.commit(registry)
        m = '__init__() missing 1 required positional argument: for_'
        assert str(exc.value).startswith(m)

    def test_predicates(self, forview_action, resourceview_action):
        first_predicates = forview_action.predicates
        assert ('for_',) == tuple(first_predicates.keys())
        second_predicates = resourceview_action.predicates
        assert ('for_', 'resource') == tuple(second_predicates.keys())

    def test_str(self, forview_action, resourceview_action):
        assert 'for_-IndexView' == forview_action.name == str(forview_action)
        assert 'for_-IndexView--resource-Resource' == str(resourceview_action)

    def test_sort_order(self, forview_action, resourceview_action):
        assert 10 == forview_action.sort_order
        assert 20 == resourceview_action.sort_order

    def test_sorted_actions(self, committed_registry):
        sorted_actions = ViewAction.sorted_actions('view', committed_registry)
        assert 2 == len(sorted_actions)
        first = sorted_actions[0][0]
        assert 'for_-IndexView--resource-Resource' == first.name

    def test_unknown_predicte(self, registry):
        @registry.view(bogus='BOGUS')
        @dataclass
        class ForView:
            logo: str = 'Logo XX'

        with pytest.raises(UnknownArgument) as exc:
            dectate.commit(registry)
        m = 'Decorator supplied unknown predicate: bogus'
        assert str(exc.value).startswith(m)


class TestPredicatesMatch:
    def test_missing_argument(self, forview_action):
        with pytest.raises(LookupMissingRequired) as exc:
            forview_action.all_predicates_match(resource=999)
        m = 'Lookup is missing required field: for_'
        assert str(exc.value).startswith(m)

    def test_unknown_argument(self, forview_action):
        with pytest.raises(UnknownLookup) as exc:
            forview_action.all_predicates_match(for_=IndexView, bogus=999)
        m = 'Lookup supplied unknown predicate argument: bogus'
        assert str(exc.value).startswith(m)

    def test_predicates_for_match(self, forview_action: ViewAction):
        assert True is forview_action.all_predicates_match(for_=IndexView)

    def test_predicates_for_not_match(self, forview_action: ViewAction):
        assert False is forview_action.all_predicates_match(for_=NotView)

    def test_predicates_resource_match(self, resourceview_action: ViewAction):
        assert True is resourceview_action.all_predicates_match(
            for_=IndexView,
            resource=Resource
        )

    def test_predicates_resource_not_match(self,
                                           resourceview_action: ViewAction):
        assert False is resourceview_action.all_predicates_match(
            for_=IndexView,
            resource=NotResource
        )

    def test_predicates_resource_not_for__match(self,
                                                resourceview_action:
                                                ViewAction):
        assert False is resourceview_action.all_predicates_match(
            for_=NotView,
            resource=Resource
        )

    def test_resourceview_action_not_handed_resource(self,
                                                     resourceview_action):
        assert False is resourceview_action.all_predicates_match(
            for_=IndexView)


class TestMultipleActions:
    def test_match_forview_action(self, registry, actions):
        for_view = actions[0][1]
        view_class = ViewAction.get_class(registry, 'view', for_=IndexView)
        assert for_view == view_class

    def test_match_resource(self, registry, actions):
        resource_view = actions[1][1]
        view_class = ViewAction.get_class(registry, 'view',
                                          for_=IndexView,
                                          resource=Resource,
                                          )
        assert resource_view == view_class

    def test_not_match_resource(self, registry, actions):
        for_view = actions[0][1]

        class Article:
            pass

        view_class = ViewAction.get_class(registry, 'view',
                                          for_=IndexView,
                                          resource=Article,
                                          )
        assert for_view == view_class

    def test_no_matches(self, registry, actions):
        view_class = ViewAction.get_class(registry, 'view',
                                          for_=NotView,
                                          resource=NotResource,
                                          )
        assert None is view_class
