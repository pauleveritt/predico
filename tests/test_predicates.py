from dataclasses import dataclass

import dectate
import pytest
from dectate import ConflictError

from kaybee_component.predicate_registry import Kaybee
from kaybee_component.predicates import ForPredicate
from kaybee_component.views import IndexView, ViewAction


@pytest.fixture
def registry():
    class PredicateApp(Kaybee):
        view = dectate.directive(ViewAction)

    return PredicateApp


@pytest.fixture
def simple_view(registry):
    @registry.view(for_=IndexView)
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

    def test_simple_registration(self, registry, simple_view):
        q = dectate.Query('view')
        actions = list(q(registry))
        assert 1 == len(actions)
        action, target = actions[0]
        assert 'for_-IndexView' == action.name
        assert 'ViewForPredicate' == action.for_.__class__.__name__
        assert target.__name__.endswith('ResourceView')


class TestConflict:
    def test_conflict_error(self, registry, simple_view):
        @registry.view(for_=IndexView)
        @dataclass
        class ArticleView:
            logo: str = 'Logo XX'

        with pytest.raises(ConflictError):
            dectate.commit(registry)


class TestFindBestMatch:
    def test_two(self, registry, simple_view, two_predicate_view):
        pass
