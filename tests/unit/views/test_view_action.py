import pytest

import dectate

from kaybee_component.views import ViewAction


@pytest.fixture
def committed_registry(registry, for_view, resource_view):
    dectate.commit(registry)
    return registry


@pytest.fixture
def actions(committed_registry):
    q = dectate.Query('view')
    actions = list(q(committed_registry))
    return actions


class TestViewAction:
    def test_import(self, actions):
        assert 'ViewAction' == ViewAction.__name__

    def test_construction(self, actions):
        assert 2 == len(actions)

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
