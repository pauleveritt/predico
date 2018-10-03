from dataclasses import dataclass

import pytest

from predico.field_types import injected
from predico.servicemanager.manager import Services
from predico.services.adapter.base_adapter import Adapter
from predico.services.request.base_request import Request
from predico.services.resource.base_resource import Resource, Resources
from predico.services.resource.service import ResourceService
from predico.services.view.base_view import View
from predico.services.view.config import ViewServiceConfig


# ---------------  Resources

@dataclass
class TestArticle(Resource):
    title: str
    parentid: str

    @property
    def parentids(self):
        return [self.parentid]


@dataclass
class TestSection(Resource):
    title: str
    parentid: str

    @property
    def parentids(self):
        return [self.parentid]


# ---------------  Views

@dataclass
class TestResourceView(View):
    viewservice_config: ViewServiceConfig
    name: str = 'Generic Resource View'


@dataclass
class TestSectionView(View):
    viewservice_config: ViewServiceConfig
    name: str = 'Section View'


@dataclass
class TestResourceIdView(View):
    viewservice_config: ViewServiceConfig
    name: str = 'One Specific Resource ID'


@dataclass
class TestParentIdView(View):
    viewservice_config: ViewServiceConfig
    name: str = 'One Specific Parent ID'


# ---------------  Adapters

@dataclass
class FakeBreadcrumbsResources:
    """ The target result of an adapter """
    pass


@dataclass
class FakeBreadcrumbsResourcesAdapter(Adapter):
    # Adapter: Should wind up on TestInjectedDefaultAdapterView
    request: Request
    resource: Resource
    resources: Resources
    name: str = 'Fake Breadcrumbs Resources'
    injected_flag: str = 'Got the attr off injected adapter'

    @property
    def resource_title(self):
        return self.resource.title


# These views are in the adapters section because it needs the
# adapter class name defined first. This first view winds up getting
# the more-general adapter FakeBreadcrumbsResources.
@dataclass
class TestInjectedDefaultAdapterView(View):
    breadcrumbs_resources: FakeBreadcrumbsResources
    viewservice_config: ViewServiceConfig
    name: str = 'Use a Default Injected Adapter'


@dataclass
class FakeArticleBreadcrumbsResourcesAdapter(Adapter):
    # ADAPTER: Should wind up on TestInjectedResourceIdAdapterView
    request: Request
    resource: Resource
    name: str = 'Fake Article Breadcrumbs Resources'

    @property
    def resource_title(self):
        return self.resource.title


# This view gets the more-specific injected adapter
# FakeArticleBreadcrumbsResources.
@dataclass
class TestInjectedResourceIdAdapterView(View):
    breadcrumbs_resources: FakeBreadcrumbsResources
    viewservice_config: ViewServiceConfig
    name: str = 'Use a ResourceId Injected Adapter'


# This view tries to get the attribute off an adapter
@dataclass
class TestInjectedResourceIdAdapterView(View):
    breadcrumbs_resources: FakeBreadcrumbsResources
    viewservice_config: ViewServiceConfig
    adapter_flag: str = injected(FakeBreadcrumbsResources,
                                 attr='injected_flag')
    name: str = 'Use a ResourceId Injected Adapter'


@dataclass
class FakeResourceIdBreadcrumbsResourcesAdapter(Adapter):
    # ADAPTER: Should wind up on TestInjectedResourceIdAdapterView
    request: Request
    resource: Resource
    name: str = 'Fake ResourceId Breadcrumbs Resources'
    injected_flag: int = 99

    @property
    def resource_title(self):
        return self.resource.title


@dataclass
class FakeParentIdBreadcrumbsResourcesAdapter(Adapter):
    request: Request
    resource: Resource
    name: str = 'Fake ParentId Breadcrumbs Resources'
    injected_flag: int = 99

    @property
    def resource_title(self):
        return self.resource.title


# Test the call=False option for injected()
class FakeNocallMarker:
    """ A marker """
    pass


@dataclass
class FakeNocallAdapter(Adapter):
    # ADAPTER: Should wind up on TestNocallAdapterView
    request: Request
    resource: Resource
    name: str = 'Fake Nocall Adapter Adapter'


@dataclass
class TestNocallAdapterView(View):
    nocall: FakeNocallAdapter = injected(FakeNocallMarker, call=False)
    name: str = 'Use a Nocall Adapter View'


@pytest.fixture
def fake_breadcrumbs_resources():
    # Use a fixture to get the right-named class into tests
    return FakeBreadcrumbsResources


# ---------------  Registration of resources, views, etc.


@pytest.fixture
def registrations(test_registry):
    # Resources
    test_registry.resource('testarticle')(TestArticle)
    test_registry.resource('testsection')(TestSection)

    # Views
    test_registry.view()(TestResourceView)
    test_registry.view(resource=TestArticle)(
        TestSectionView)
    test_registry.view(resourceid='more/specificid')(
        TestResourceIdView)
    test_registry.view(parentid='more/index',
                       resource=TestArticle
                       )(TestParentIdView)
    # Adapter-related views
    test_registry.view(resourceid='injected/defaultadapter',
                       resource=TestArticle
                       )(TestInjectedDefaultAdapterView)
    test_registry.view(resourceid='injected/resourceidadapter',
                       resource=TestArticle
                       )(TestInjectedResourceIdAdapterView)
    test_registry.view(resourceid='pydantic/injectedattr',
                       )(TestInjectedResourceIdAdapterView)
    test_registry.view(resourceid='nocall/index',
                       )(TestNocallAdapterView)

    # Adapters
    test_registry.adapter(
        for_=FakeBreadcrumbsResources,
    )(FakeBreadcrumbsResourcesAdapter)
    test_registry.adapter(
        for_=FakeBreadcrumbsResources,
        resource=TestArticle
    )(FakeArticleBreadcrumbsResourcesAdapter)
    test_registry.adapter(
        for_=FakeBreadcrumbsResources,
        resourceid='injected/resourceidadapter'
    )(FakeResourceIdBreadcrumbsResourcesAdapter)
    test_registry.adapter(
        for_=FakeBreadcrumbsResources,
        parentid='pydantic/index'
    )(FakeParentIdBreadcrumbsResourcesAdapter)
    # The Nocall adapter
    test_registry.adapter(for_=FakeNocallMarker)(FakeNocallAdapter)


@pytest.fixture
def services(initialized_sm) -> Services:
    services: Services = initialized_sm.services
    return services


@pytest.fixture
def rs(services) -> ResourceService:
    r: ResourceService = services['resource']
    return r


@pytest.fixture
def test_resources(rs):
    """ Add some fake content to the resource service """
    rs.add_resource(rtype='testsection', id='about/index',
                    title='About Section', parentid='index')

    rs.add_resource(rtype='testsection', id='more/index',
                    title='More Section', parentid='more/index')

    rs.add_resource(rtype='testarticle', id='news/first',
                    title='Contact', parentid='news/index')

    rs.add_resource(rtype='testarticle', id='more/contact',
                    title='Contact', parentid='more/index')

    rs.add_resource(rtype='testarticle', id='more/specificid',
                    title='Specific', parentid='more/index')

    rs.add_resource(rtype='testarticle', id='injected/defaultadapter',
                    title='Injected Default Adapter Article',
                    parentid='injected/index')

    rs.add_resource(rtype='testarticle', id='injected/resourceidadapter',
                    title='Injected ResourceId Adapter Article',
                    parentid='injected/index')

    rs.add_resource(rtype='testsection', id='pydantic/about',
                    title='Pydantic Section', parentid='pydantic/index')

    rs.add_resource(rtype='testsection', id='pydantic/injectedattr',
                    title='Pydantic Injectedattr Section',
                    parentid='pydantic/index')

    rs.add_resource(rtype='testsection', id='nocall/index',
                    title='Nocall Adapter',
                    parentid='index')
