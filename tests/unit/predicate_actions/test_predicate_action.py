from dataclasses import dataclass

import dectate
import pytest
from dectate import DirectiveReportError

from kaybee_component.resources import Resource
from kaybee_component.views import ViewAction
from kaybee_component.viewtypes import IndexView


class NotView:
    pass


class NotResource:
    pass


@pytest.fixture
def committed_registry(registry, for_view, resource_view):
    dectate.commit(registry)
    return registry


@pytest.fixture
def actions(committed_registry):
    q = dectate.Query('view')
    actions = list(q(committed_registry))
    return actions


@pytest.fixture
def first_action(actions) -> ViewAction:
    return actions[0][0]


@pytest.fixture
def second_action(actions) -> ViewAction:
    return actions[1][0]


class TestViewAction:
    def test_import(self, actions):
        assert 'ViewAction' == ViewAction.__name__

    def test_missing_for(self, registry):
        @registry.view()
        @dataclass
        class ForView:
            logo: str = 'Logo XX'

        with pytest.raises(DirectiveReportError) as exc:
            dectate.commit(registry)
        m = '__init__() missing 1 required positional argument: for_'
        assert str(exc.value).startswith(m)

    def test_construction(self, actions):
        assert 2 == len(actions)

    def test_predicates(self, actions):
        first_action: ViewAction = actions[0][0]
        first_predicates = first_action.predicates
        assert ('for_',) == tuple(first_predicates.keys())
        second_action = actions[1][0]
        second_predicates = second_action.predicates
        assert ('for_', 'resource') == tuple(second_predicates.keys())

    def test_str(self, actions):
        first_action = actions[0][0]
        assert 'for_-IndexView' == first_action.name == str(first_action)
        second_action = actions[1][0]
        assert 'for_-IndexView--resource-Resource' == str(second_action)

    def test_sort_order(self, actions):
        first_action = actions[0][0]
        assert 10 == first_action.sort_order
        second_action = actions[1][0]
        assert 20 == second_action.sort_order

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

        with pytest.raises(DirectiveReportError) as exc:
            dectate.commit(registry)
        m = 'Decorator supplied unknown predicate: bogus'
        assert str(exc.value).startswith(m)


class TestPredicatesMatch:
    def test_missing_argument(self, first_action):
        with pytest.raises(TypeError) as exc:
            first_action.all_predicates_match(resource=999)
        m = 'Lookup is missing required field: for_'
        assert str(exc.value).startswith(m)

    def test_unknown_argument(self, first_action):
        with pytest.raises(TypeError) as exc:
            first_action.all_predicates_match(for_=IndexView, bogus=999)
        m = 'Lookup supplied unknown predicate argument: bogus'
        assert str(exc.value).startswith(m)

    def test_predicates_for_match(self, first_action: ViewAction):
        assert True is first_action.all_predicates_match(for_=IndexView)

    def test_predicates_for_not_match(self, first_action: ViewAction):
        assert False is first_action.all_predicates_match(for_=NotView)

    def test_predicates_resource_match(self, second_action: ViewAction):
        assert True is second_action.all_predicates_match(
            for_=IndexView,
            resource=Resource
        )

    def test_predicates_resource_not_match(self, second_action: ViewAction):
        assert False is second_action.all_predicates_match(
            for_=IndexView,
            resource=NotResource
        )

    def test_predicates_resource_not_for__match(self,
                                                second_action: ViewAction):
        assert False is second_action.all_predicates_match(
            for_=NotView,
            resource=Resource
        )

    def test_second_action_not_handed_resource(self, second_action):
        assert False is second_action.all_predicates_match(for_=IndexView)


class TestMultipleActions:
    def test_match_first_action(self, registry, actions):
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
