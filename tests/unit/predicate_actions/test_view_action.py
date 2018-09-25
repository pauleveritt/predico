from tests.unit.predicate_actions.conftest import (
    NotView,
    NotResource,
    TestViewAction
)


def test_match_forview_action(registry, actions, testindexview):
    for_view = actions[0][1]
    view_class = TestViewAction.get_class(None, registry, for_=testindexview)
    assert for_view == view_class


def test_match_resource(registry, actions, testindexview, testresource):
    resource_view = actions[1][1]
    view_class = TestViewAction.get_class(None, registry,
                                          for_=testindexview,
                                          resource=testresource,
                                          )
    assert resource_view == view_class


def test_not_match_resource(registry, actions, testindexview):
    for_view = actions[0][1]

    class Article:
        pass

    view_class = TestViewAction.get_class(None, registry,
                                          for_=testindexview,
                                          resource=Article,
                                          )
    assert for_view == view_class


def test_no_matches(registry, actions):
    view_class = TestViewAction.get_class(None, registry,
                                          for_=NotView,
                                          resource=NotResource,
                                          )
    assert None is view_class
