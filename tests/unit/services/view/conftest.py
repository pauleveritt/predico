from dataclasses import dataclass, field
from typing import List

import dectate
import pytest

from predico.servicemanager.action import ServiceAction
from predico.servicemanager.manager import ServiceManager
from predico.services.request.base_request import Request
from predico.services.resource.base_resource import Resource
from predico.services.view.action import ViewAction
from predico.services.view.base_view import IndexView
from predico.services.view.service import ViewService


@dataclass
class FakeResource(Resource):
    id: str = 'more/resource1'
    rtype: str = 'resource'
    parentids: List[str] = field(default_factory=list)


@pytest.fixture
def fake_resource1():
    fr1 = FakeResource(parentids=['more/index', 'index'])
    return fr1


@dataclass
class FakeArticle(Resource):
    id: str = 'more/article1'
    rtype: str = 'article'
    parentids: List[str] = field(default_factory=list)


@pytest.fixture
def fake_article1():
    fa1 = FakeArticle(parentids=['more/index', 'index'])
    return fa1


@pytest.fixture
def fake_article2():
    # Used for matching resourceid
    fa1 = FakeArticle(id='more/article2', parentids=['more/index', 'index'])
    return fa1


@dataclass
class FakeBlog(Resource):
    id: str = 'blog/blog1'
    rtype: str = 'blog'
    parentids: List[str] = field(default_factory=list)


@pytest.fixture
def fake_blog1():
    fb1 = FakeBlog(parentids=['blog/index', 'index'])
    return fb1


@dataclass
class FakeRequest(Request):
    resource: Resource


@pytest.fixture
def fake_request_class():
    # Fix problems with importing from tests.unit.*
    return FakeRequest


@pytest.fixture
def sm_registry():
    """ Provide test isolation for builtin service registry """

    class FakeServiceRegistry(dectate.App):
        service = dectate.directive(ServiceAction)
        view = dectate.directive(ViewAction)

    return FakeServiceRegistry


@pytest.fixture
def uninitialized_sm(sm_config, sm_registry) -> ServiceManager:
    """ Make a ServiceManager """

    sm = ServiceManager(sm_config, sm_registry)
    sm.registry = sm_registry
    return sm


# -------------------------------------------
# Registrations
#
# - Some view registrations
# - Some resource registrations
# - etc.
# -------------------------------------------


@pytest.fixture
def register_service(sm_registry):
    sm_registry.service(name='view')(ViewService)


@dataclass
class FakeForView1:
    name: str = 'Fake For View'


@pytest.fixture
def fakefor_view(sm_registry):
    sm_registry.view(for_=IndexView)(FakeForView1)


@dataclass
class FakeResourceView:
    name: str = 'Fake Resource View'


@pytest.fixture
def fakeresource_view(sm_registry):
    sm_registry.view(for_=IndexView, resource=FakeResource)(
        FakeResourceView)


@dataclass
class FakeArticleView:
    name: str = 'Fake Article View'


@pytest.fixture
def fakearticle_view(sm_registry):
    sm_registry.view(for_=IndexView, resource=FakeArticle)(
        FakeArticleView)


@dataclass
class FakeResourceIdView:
    name: str = 'Fake ResourceId View'


@pytest.fixture
def fakeresourceid_view(sm_registry):
    sm_registry.view(for_=IndexView, resourceid='more/article2')(
        FakeResourceIdView)


@dataclass
class FakeParentIdView:
    name: str = 'Fake ParentId View'


@pytest.fixture
def fakeparentid_view(sm_registry):
    sm_registry.view(for_=IndexView, parentid='more/index')(
        FakeParentIdView)


@pytest.fixture
def registrations():
    return


@pytest.fixture
def initialized_sm(uninitialized_sm, register_service, registrations):
    """ The equivalent of an app with commit """
    uninitialized_sm.initialize()
    return uninitialized_sm


@pytest.fixture
def services(initialized_sm):
    return initialized_sm.services


@pytest.fixture
def viewservice(services) -> ViewService:
    return services['view']
