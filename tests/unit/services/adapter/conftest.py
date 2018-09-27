from dataclasses import dataclass, field
from typing import List

import dectate
import pytest

from kaybee_component.servicemanager.action import ServiceAction
from kaybee_component.servicemanager.manager import ServiceManager
from kaybee_component.services.adapter.action import AdapterAction
from kaybee_component.services.adapter.service import AdapterService
from kaybee_component.services.request.base_request import Request
from kaybee_component.services.resource.base_resource import Resource


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
    return FakeRequest


@pytest.fixture
def sm_registry():
    """ Provide test isolation for builtin service registry """

    class FakeServiceRegistry(dectate.App):
        service = dectate.directive(ServiceAction)
        adapter = dectate.directive(AdapterAction)

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
# - Some adapter registrations
# - Some resource registrations
# - etc.
# -------------------------------------------


@pytest.fixture
def register_service(sm_registry):
    sm_registry.service(name='adapter')(AdapterService)


@dataclass
class FakeBreadcrumbsResources:
    """ The kind of adapter we're interested in """
    name: str = 'Fake Breadcrumbs Resources'


@pytest.fixture
def fake_breadcrumbs_resources():
    # Use a fixture to get the right-named class into tests
    return FakeBreadcrumbsResources


@pytest.fixture
def fakefor_adapter(sm_registry):
    sm_registry.adapter(for_=FakeBreadcrumbsResources)(
        FakeBreadcrumbsResources)


@dataclass
class FakeResourceAdapter:
    name: str = 'Fake Resource Adapter'


@pytest.fixture
def fakeresource_adapter(sm_registry):
    sm_registry.adapter(for_=FakeBreadcrumbsResources, resource=FakeResource)(
        FakeResourceAdapter)


@dataclass
class FakeArticleAdapter:
    name: str = 'Fake Article Adapter'


@pytest.fixture
def fakearticle_adapter(sm_registry):
    sm_registry.adapter(for_=FakeBreadcrumbsResources, resource=FakeArticle)(
        FakeArticleAdapter)


@dataclass
class FakeResourceIdAdapter:
    name: str = 'Fake ResourceId Adapter'


@pytest.fixture
def fakeresourceid_adapter(sm_registry):
    sm_registry.adapter(for_=FakeBreadcrumbsResources,
                        resourceid='more/article2')(
        FakeResourceIdAdapter)


@dataclass
class FakeParentIdAdapter:
    name: str = 'Fake ParentId Adapter'


@pytest.fixture
def fakeparentid_adapter(sm_registry):
    sm_registry.adapter(for_=FakeBreadcrumbsResources, parentid='more/index')(
        FakeParentIdAdapter)


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
def adapterservice(services) -> AdapterService:
    return services['adapter']
