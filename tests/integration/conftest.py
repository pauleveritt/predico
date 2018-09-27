from dataclasses import dataclass

import pytest

from kaybee_component.servicemanager.manager import Services
from kaybee_component.services.request.base_request import Request
from kaybee_component.services.resource.base_resource import Resource
from kaybee_component.services.resource.service import ResourceService
from kaybee_component.services.view.base_view import IndexView
from kaybee_component.services.view.config import ViewServiceConfig


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
class TestResourceView:
    viewservice_config: ViewServiceConfig
    name: str = 'Generic Resource View'


@dataclass
class TestSectionView:
    viewservice_config: ViewServiceConfig
    name: str = 'Section View'


@dataclass
class TestResourceIdView:
    viewservice_config: ViewServiceConfig
    name: str = 'One Specific Resource ID'


@dataclass
class TestParentIdView:
    viewservice_config: ViewServiceConfig
    name: str = 'One Specific Parent ID'


# ---------------  Adapters


@dataclass
class FakeBreadcrumbsResources:
    request: Request
    resource: Resource
    name: str = 'Fake Breadcrumbs Resources'

    @property
    def resource_title(self):
        return self.resource.title


# These views are in the adapters section because it needs the
# adapter class name defined first.
@dataclass
class TestInjectedDefaultAdapterView:
    breadcrumbs_resources: FakeBreadcrumbsResources
    viewservice_config: ViewServiceConfig
    name: str = 'Use a Default Injected Adapter'


@dataclass
class TestInjectedResourceIdAdapterView:
    breadcrumbs_resources: FakeBreadcrumbsResources
    viewservice_config: ViewServiceConfig
    name: str = 'Use a ResourceId Injected Adapter'


@dataclass
class FakeArticleBreadcrumbsResources:
    request: Request
    resource: Resource
    name: str = 'Fake Article Breadcrumbs Resources'

    @property
    def resource_title(self):
        return self.resource.title


@dataclass
class FakeResourceIdBreadcrumbsResources:
    request: Request
    resource: Resource
    name: str = 'Fake ResourceId Breadcrumbs Resources'

    @property
    def resource_title(self):
        return self.resource.title


@dataclass
class FakeParentIdBreadcrumbsResources:
    request: Request
    resource: Resource
    name: str = 'Fake ParentId Breadcrumbs Resources'

    @property
    def resource_title(self):
        return self.resource.title


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
    test_registry.view(for_=IndexView)(TestResourceView)
    test_registry.view(for_=IndexView, resource=TestArticle)(
        TestSectionView)
    test_registry.view(for_=IndexView, resourceid='more/specificid')(
        TestResourceIdView)
    test_registry.view(for_=IndexView, parentid='more/index',
                       resource=TestArticle
                       )(TestParentIdView)
    # Adapter-related views
    test_registry.view(for_=IndexView, resourceid='injected/defaultadapter',
                       resource=TestArticle
                       )(TestInjectedDefaultAdapterView)
    test_registry.view(for_=IndexView, resourceid='injected/resourceidadapter',
                       resource=TestArticle
                       )(TestInjectedResourceIdAdapterView)

    # Adapters
    test_registry.adapter(
        for_=FakeBreadcrumbsResources,
    )(FakeBreadcrumbsResources)
    test_registry.adapter(
        for_=FakeBreadcrumbsResources,
        resource=TestArticle
    )(FakeArticleBreadcrumbsResources)
    test_registry.adapter(
        for_=FakeBreadcrumbsResources,
        resourceid='more/specificid'
    )(FakeResourceIdBreadcrumbsResources)
    test_registry.adapter(
        for_=FakeBreadcrumbsResources,
        parentid='more/index'
    )(FakeParentIdBreadcrumbsResources)


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
