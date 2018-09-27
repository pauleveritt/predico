from dataclasses import dataclass

import dectate
import pytest

from kaybee_component.servicemanager.action import ServiceAction
from kaybee_component.services.resource.action import ResourceAction
from kaybee_component.services.resource.base_resource import Resource
from kaybee_component.services.resource.service import ResourceService


@pytest.fixture
def sm_registry():
    """ Provide test isolation for builtin service registry """

    class FakeServiceRegistry(dectate.App):
        service = dectate.directive(ServiceAction)
        resource = dectate.directive(ResourceAction)

    return FakeServiceRegistry


@pytest.fixture
def register_service(sm_registry):
    sm_registry.service(name='resource')(ResourceService)


@pytest.fixture
def registrations(sm_registry):
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
def resourceservice(services) -> ResourceService:
    return services['resource']


# ---------------  Resources

@dataclass
class TestArticle(Resource):
    title: str
    parentid: str

    @property
    def parentids(self):
        return [self.parentid]


@pytest.fixture()
def fake_article(uninitialized_sm):
    registry = uninitialized_sm.registry
    registry.resource('testarticle')(TestArticle)


@pytest.fixture()
def fake_section(uninitialized_sm):
    registry = uninitialized_sm.registry
    registry.resource('testsection')(TestSection)


@dataclass
class TestSection(Resource):
    title: str
    parentid: str

    @property
    def parentids(self):
        return [self.parentid]


@pytest.fixture
def test_resources(resourceservice):
    """ Add some fake content to the resource service """

    resourceservice.add_resource(rtype='testsection', id='more/index',
                                 title='More Section', parentid='more/index')

    resourceservice.add_resource(rtype='testarticle', id='news/first',
                                 title='Contact', parentid='news/index')

    resourceservice.add_resource(rtype='testarticle', id='more/contact',
                                 title='Contact', parentid='more/index')

    resourceservice.add_resource(rtype='testarticle', id='more/specificid',
                                 title='Specific', parentid='more/index')
