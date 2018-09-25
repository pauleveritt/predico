from dataclasses import dataclass

import pytest

from kaybee_component.service.manager import Services
from kaybee_component.services.resource.base_resource import Resource
from kaybee_component.services.resource.service import ResourceService


@pytest.fixture
def registrations(test_article):
    pass


@dataclass
class TestArticle(Resource):
    title: str


@dataclass
class TestSection(Resource):
    title: str


@pytest.fixture
def testarticle_class():
    return TestArticle


@pytest.fixture
def testsection_class():
    return TestSection


@pytest.fixture
def test_article(test_registry, testarticle_class):
    test_registry.resource('testarticle')(testarticle_class)


@pytest.fixture
def test_section(test_registry, testsection_class):
    test_registry.resource('testsection')(testsection_class)


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
    rs.add_resource(rtype='testsection', id='more/index', title='More Section')
    rs.add_resource(rtype='testarticle', id='more/contact', title='Contact')
    rs.add_resource(rtype='testarticle', id='more/specificid',
                    title='Specific')
