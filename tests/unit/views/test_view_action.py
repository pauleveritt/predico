from dataclasses import dataclass

import dectate
import pytest
from dectate import DirectiveReportError

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

    def test_missing_for(self, registry):
        @registry.view()
        @dataclass
        class ForView:
            logo: str = 'Logo XX'

        with pytest.raises(DirectiveReportError) as exc:
            dectate.commit(registry)
        m = '__init__() missing 1 required positional argument: \'for_\''
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
