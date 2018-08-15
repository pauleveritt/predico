from dataclasses import dataclass

import dectate
import pytest
from dectate import ConflictError

from kaybee_component.predicate_registry import Kaybee
from kaybee_component.predicates import ForPredicate, ResourcePredicate
from kaybee_component.resources import Resource
from kaybee_component.views import IndexView, ViewAction


@pytest.fixture
def registry():
    class PredicateApp(Kaybee):
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


@pytest.fixture
def two_predicate_view(registry):
    return

    @registry.view(for_=IndexView)
    @dataclass
    class ArticleView:
        logo: str = 'Logo XX'


class TestForPredicate:
    def test_import(self):
        assert 'ForPredicate' == ForPredicate.__name__

    def test_construction(self):
        predicate = ForPredicate(value=IndexView)
        assert 'for_' == predicate.key

    def test_simple_registration(self, registry, for_view):
        q = dectate.Query('view')
        actions = list(q(registry))
        assert 1 == len(actions)
        action, target = actions[0]
        assert 'for_-IndexView' == action.name
        assert 'ViewForPredicate' == action.for_.__class__.__name__
        assert 10 == action.sort_order
        assert target.__name__.endswith('ForView')


class TestResourcePredicate:
    def test_import(self):
        assert 'ResourcePredicate' == ResourcePredicate.__name__

    def test_construction(self):
        predicate = ResourcePredicate(value=Resource)
        assert 'resource' == predicate.key

    def test_simple_registration(self, registry, resource_view):
        q = dectate.Query('view')
        actions = list(q(registry))
        assert 1 == len(actions)
        action, target = actions[0]
        assert 'for_-IndexView--resource-Resource' == action.name
        assert 'ViewForPredicate' == action.for_.__class__.__name__
        assert 20 == action.sort_order
        assert target.__name__.endswith('ResourceView')


class TestConflict:
    def test_conflict_error(self, registry, for_view):
        @registry.view(for_=IndexView)
        @dataclass
        class ArticleView:
            logo: str = 'Logo XX'

        with pytest.raises(ConflictError):
            dectate.commit(registry)


class TestTwoViews:
    def test_two(self, registry, for_view, resource_view):
        q = dectate.Query('view')
        actions = list(q(registry))
        assert 2 == len(actions)

    def test_sorting(self, registry, for_view, resource_view):
        sorted_actions = ViewAction.sorted_actions(registry)
        assert 2 == len(sorted_actions)
        first = sorted_actions[0][0]
        assert 'for_-IndexView--resource-Resource' == first.name

    def test_select_resource_view(self, registry, for_view, resource_view):
        sorted_actions = ViewAction.sorted_actions(registry)
        resource_class = sorted_actions[0][0].resource.value
        resource_view = sorted_actions[0][1]
        view_class = ViewAction.get_class(registry,
                                          resource_target=resource_class)
        assert resource_view == view_class

    def test_select_for_view(self, registry, for_view, resource_view):
        sorted_actions = ViewAction.sorted_actions(registry)
        resource_view = sorted_actions[1][1]
        view_class = ViewAction.get_class(registry)
        assert resource_view == view_class
