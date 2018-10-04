from dataclasses import dataclass, field
from typing import List

import dectate
import pytest

from predico.servicemanager.action import ServiceAction
from predico.servicemanager.manager import ServiceManager
from predico.services.adapter.action import AdapterAction
from predico.services.adapter.base_adapter import Adapter
from predico.services.adapter.service import AdapterService
from predico.services.request.base_request import Request
from predico.services.resource.base_resource import Resource


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
    fa1 = FakeArticle(id='more/article2', parentids=['more/index', 'index'])
    return fa1


@pytest.fixture
def fake_article2():
    # Used for matching resourceid
    fa2 = FakeArticle(id='more/article2', parentids=['more/index', 'index'])
    return fa2


@pytest.fixture
def fake_article3():
    # Used for testing request.adapt_resource
    fa3 = FakeArticle(id='subrequest', parentids=['index'])
    return fa3


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
    """ The result of an adapter for getting breadcrumbs """
    pass


@dataclass
class FakeBreadcrumbsResourcesAdapter(Adapter):
    """ The kind of adapter we're interested in """
    name: str = 'Fake Breadcrumbs Resources'

    def __call__(self):
        return self.name


@dataclass
class FakeReferenceEntry:
    """ The result of an adapter for getting breadcrumbs """
    pass


@dataclass
class FakeSubresourceAdapter(Adapter):
    """ Test passing in resource via request.adapt_resource """
    resource: Resource
    name: str = 'Fake Subresource Adapter'

    def __call__(self):
        return self.name


@pytest.fixture
def fake_breadcrumbs_resources():
    # Use a fixture to get the right-named class into tests
    return FakeBreadcrumbsResources


@pytest.fixture
def fake_reference_entry():
    # Use a fixture to get the right-named class into tests
    return FakeReferenceEntry


@pytest.fixture
def fakefor_adapter(sm_registry):
    sm_registry.adapter(for_=FakeBreadcrumbsResources)(
        FakeBreadcrumbsResourcesAdapter)


@dataclass
class FakeResourceAdapter(Adapter):
    name: str = 'Fake Resource Adapter'


@pytest.fixture
def fakeresource_adapter(sm_registry):
    sm_registry.adapter(for_=FakeBreadcrumbsResources,
                        resource=FakeResource)(
        FakeResourceAdapter)


@dataclass
class FakeArticleAdapter(Adapter):
    name: str = 'Fake Article Adapter'

    def __call__(self):
        return self.name


@pytest.fixture
def fakearticle_adapter(sm_registry):
    sm_registry.adapter(for_=FakeBreadcrumbsResources,
                        resource=FakeArticle)(
        FakeArticleAdapter)


@pytest.fixture
def fakesubresource_adapter(sm_registry):
    sm_registry.adapter(for_=FakeReferenceEntry)(FakeSubresourceAdapter)


@dataclass
class FakeResourceIdAdapter(Adapter):
    name: str = 'Fake ResourceId Adapter'

    def __call__(self):
        return self.name


@pytest.fixture
def fakeresourceid_adapter(sm_registry):
    sm_registry.adapter(for_=FakeBreadcrumbsResources,
                        resourceid='more/article2')(
        FakeResourceIdAdapter)


@dataclass
class FakeParentIdAdapter(Adapter):
    name: str = 'Fake ParentId Adapter'


@pytest.fixture
def fakeparentid_adapter(sm_registry):
    sm_registry.adapter(for_=FakeBreadcrumbsResources,
                        parentid='more/index')(
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
