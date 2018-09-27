from dataclasses import dataclass

import pytest

from kaybee_component.servicemanager.manager import Services
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
    rs.add_resource(rtype='testsection', id='more/index',
                    title='More Section', parentid='more/index')

    rs.add_resource(rtype='testarticle', id='news/first',
                    title='Contact', parentid='news/index')

    rs.add_resource(rtype='testarticle', id='more/contact',
                    title='Contact', parentid='more/index')

    rs.add_resource(rtype='testarticle', id='more/specificid',
                    title='Specific', parentid='more/index')
