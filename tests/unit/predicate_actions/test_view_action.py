from tests.unit.predicate_actions.conftest import (
    NotView,
    NotResource,
    TestViewAction
)


def test_match_forview_action(request, actions, testindexview):
    for_view = actions[0][1]
    view_class = TestViewAction.get_class(request, for_=testindexview)
    assert for_view == view_class


def test_match_resource(request, actions, testindexview, testresource):
    resource_view = actions[1][1]
    view_class = TestViewAction.get_class(request,
                                          for_=testindexview,
                                          resource=testresource,
                                          )
    assert resource_view == view_class


def test_not_match_resource(request, actions, testindexview):
    for_view = actions[0][1]

    class Article:
        pass

    view_class = TestViewAction.get_class(request,
                                          for_=testindexview,
                                          resource=Article,
                                          )
    assert for_view == view_class


def test_no_matches(request, actions):
    view_class = TestViewAction.get_class(request,
                                          for_=NotView,
                                          resource=NotResource,
                                          )
    assert None is view_class
