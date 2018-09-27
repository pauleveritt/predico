# from dataclasses import dataclass
# from typing import Mapping, Union
#
# import dectate
# import pytest
#
# from kaybee_component.predicates import ForPredicate, ResourcePredicate
# from kaybee_component.services.view.action import PredicateAction
#
#
# @dataclass
# class Resource:
#     pass
#
#
# class NotView:
#     pass
#
#
# class NotResource:
#     pass
#
#
# class TestIndexView:
#     pass
#
#
# @pytest.fixture
# def testindexview():
#     # Bleh, different import paths generate different equality
#     return TestIndexView
#
#
# @pytest.fixture
# def testresource():
#     # Bleh, different import paths generate different equality
#     return Resource
#
#
# class TestViewAction(PredicateAction):
#     action_name = 'view'
#     REQUIRED_PREDICATES = (ForPredicate,)
#     OPTIONAL_PREDICATES = (ResourcePredicate,)
#     predicates: Mapping[str, Union[ForPredicate, ResourcePredicate]]
#
#
# @dataclass
# class TestForView:
#     logo: str = 'Logo XX'
#
#
# @dataclass
# class TestResourceView:
#     logo: str = 'Logo XX'
#
#
# @pytest.fixture
# def registry():
#     class PredicateApp(dectate.App):
#         view = dectate.directive(TestViewAction)
#
#     return PredicateApp
#
#
# @pytest.fixture
# def for_view(registry):
#     registry.view(for_=TestIndexView)(TestForView)
#
#
# @pytest.fixture
# def resource_view(registry):
#     registry.view(for_=TestIndexView, resource=Resource)(TestResourceView)
#
#
# @pytest.fixture
# def committed_registry(registry, for_view, resource_view):
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
# def forview_action(actions) -> TestViewAction:
#     return actions[0][0]
#
#
# @pytest.fixture
# def resourceview_action(actions) -> TestViewAction:
#     return actions[1][0]
#
# @pytest.fixture
# def request(registry):
#     class Request:
#         pass
#
#     r = Request()
#     r.registry = registry
#     return r
