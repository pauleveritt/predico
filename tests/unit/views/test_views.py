import dectate

from kaybee_component.views import ViewAction


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

    # def test_select_for_view(self, registry, for_view, resource_view):
    #     sorted_actions = ViewAction.sorted_actions(registry)
    #     for_view = sorted_actions[1][1]
    #     view_class = ViewAction.get_class(registry, for_target=IndexView)
    #     assert for_view == view_class
