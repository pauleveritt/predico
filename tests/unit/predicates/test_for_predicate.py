import pytest

from kaybee_component.predicates import ForPredicate
from kaybee_component.services.request.base_request import Request


class FakeRequest(Request):
    pass


@pytest.fixture
def test_request():
    tr = FakeRequest()
    return tr


class TestIndexView:
    pass


@pytest.fixture
def for_predicate():
    fp = ForPredicate(TestIndexView)
    return fp


def test_construction(for_predicate):
    assert TestIndexView == for_predicate.value
    assert 'for_' == for_predicate.key
    assert 10 == for_predicate.rank


def test_str(for_predicate):
    assert 'for_-TestIndexView' == str(for_predicate)


def test_matches(for_predicate, test_request):
    assert for_predicate.matches(test_request, for_=TestIndexView)


def test_not_matches(for_predicate, test_request):
    class BadView:
        pass

    assert not for_predicate.matches(test_request, for_=BadView)

# import dectate
# import pytest
# from dectate import ConflictError
#
# from kaybee_component.predicates import ForPredicate
# from tests.unit.predicate_actions.conftest import TestIndexView
#
#
# @pytest.fixture
# def committed_registry(registry, for_view):
#     dectate.commit(registry)
#     return registry
#
#
# @pytest.fixture
# def actions(committed_registry):
#     q = dectate.Query('view')
#     actions = list(q(committed_registry))
#     return actions
#
#
# @pytest.fixture
# def first_action(actions):
#     return actions[0][0]
#
#
# def test_construction():
#     predicate = ForPredicate(value=TestIndexView, action=None)
#     assert 'for_' == predicate.key
#     assert TestIndexView == predicate.value
#     assert 10 == predicate.rank
#
#
# def test_simple_registration(actions):
#     assert 1 == len(actions)
#     action, target = actions[0]
#     assert 'for_-TestIndexView' == action.name
#     for_ = action.predicates['for_']
#     assert 'ViewForPredicate' == for_.__class__.__name__
#     assert 10 == action.sort_order
#     assert target.__name__.endswith('ForView')
#
#
# def test_str(first_action):
#     for_ = first_action.predicates['for_']
#     assert 'for_-TestIndexView' == str(for_)
#
#
# def test_matches(first_action):
#     for_ = first_action.predicates['for_']
#     view_class = for_.value
#     assert for_.matches(view_class)
#
#
# def test_not_matches(first_action):
#     for_ = first_action.predicates['for_']
#
#     class OtherView:
#         pass
#
#     assert not for_.matches(OtherView)
#
#
# def test_conflict_error_for(generate_conflict_for):
#     with pytest.raises(ConflictError):
#         generate_conflict_for()
