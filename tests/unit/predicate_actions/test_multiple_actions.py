from kaybee_component.services.resource.base_resource import Resource
from kaybee_component.services.view.action import ViewAction
from kaybee_component.services.view.base_view import IndexView
from tests.unit.predicate_actions.conftest import NotView, NotResource


def test_match_forview_action(registry, actions):
    for_view = actions[0][1]
    view_class = ViewAction.get_class(registry, 'view', for_=IndexView)
    assert for_view == view_class


def test_match_resource(registry, actions):
    resource_view = actions[1][1]
    view_class = ViewAction.get_class(registry, 'view',
                                      for_=IndexView,
                                      resource=Resource,
                                      )
    assert resource_view == view_class


def test_not_match_resource(registry, actions):
    for_view = actions[0][1]

    class Article:
        pass

    view_class = ViewAction.get_class(registry, 'view',
                                      for_=IndexView,
                                      resource=Article,
                                      )
    assert for_view == view_class


def test_no_matches(registry, actions):
    view_class = ViewAction.get_class(registry, 'view',
                                      for_=NotView,
                                      resource=NotResource,
                                      )
    assert None is view_class
