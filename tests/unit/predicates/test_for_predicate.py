from dataclasses import dataclass

import dectate
import pytest
from dectate import ConflictError

from kaybee_component.predicates import ForPredicate


@pytest.fixture
def committed_registry(registry, for_view):
    dectate.commit(registry)
    return registry


@pytest.fixture
def actions(committed_registry):
    q = dectate.Query('view')
    actions = list(q(committed_registry))
    return actions


@pytest.fixture
def first_action(actions):
    return actions[0][0]


def test_construction(testindexview):
    predicate = ForPredicate(value=testindexview, action=None)
    assert 'for_' == predicate.key
    assert testindexview == predicate.value
    assert 10 == predicate.rank


def test_simple_registration(actions):
    assert 1 == len(actions)
    action, target = actions[0]
    assert 'for_-TestIndexView' == action.name
    for_ = action.predicates['for_']
    assert 'ViewForPredicate' == for_.__class__.__name__
    assert 10 == action.sort_order
    assert target.__name__.endswith('ForView')


def test_str(first_action):
    for_ = first_action.predicates['for_']
    assert 'for_-TestIndexView' == str(for_)


def test_matches(first_action):
    for_ = first_action.predicates['for_']
    view_class = for_.value
    assert for_.matches(view_class)


def test_not_matches(first_action):
    for_ = first_action.predicates['for_']

    class OtherView:
        pass

    assert not for_.matches(OtherView)


def test_conflict_error(committed_registry, testindexview):
    @committed_registry.view(for_=testindexview)
    @dataclass
    class ArticleView:
        logo: str = 'Logo XX'

    with pytest.raises(ConflictError):
        dectate.commit(committed_registry)
