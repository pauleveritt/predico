import dectate
import pytest

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


class TestTwoViews:
    def test_two(self, actions):
        assert 2 == len(actions)

    # def test_select_resource_view(self, committed_registry):
    #     sorted_actions = ViewAction.sorted_actions(committed_registry)
    #     resource_class = sorted_actions[0][0].resource.value
    #     resource_view = sorted_actions[0][1]
    #     view_class = ViewAction.get_class(committed_registry,
    #                                       resource_target=resource_class)
    #     assert resource_view == view_class
    #
    # def test_select_for_view(self, registry, for_view, resource_view):
    #     sorted_actions = ViewAction.sorted_actions(registry)
    #     for_view = sorted_actions[1][1]
    #     view_class = ViewAction.get_class(registry, for_target=IndexView)
    #     assert for_view == view_class
