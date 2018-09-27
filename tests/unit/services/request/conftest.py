from dataclasses import field, dataclass
from typing import List

import dectate
import pytest

from kaybee_component.servicemanager.action import ServiceAction
from kaybee_component.servicemanager.manager import ServiceManager
from kaybee_component.services.request.action import RequestAction
from kaybee_component.services.request.service import RequestService
from kaybee_component.services.resource.action import ResourceAction
from kaybee_component.services.resource.base_resource import Resource
from kaybee_component.services.resource.service import ResourceService
from kaybee_component.services.view.action import ViewAction
from kaybee_component.services.view.base_view import IndexView
from kaybee_component.services.view.service import ViewService


@dataclass
class FakeArticle(Resource):
    id: str = 'more/article1'
    rtype: str = 'article'
    parentids: List[str] = field(default_factory=list)


@pytest.fixture
def fake_article1():
    fa1 = FakeArticle(parentids=['more/index', 'index'])
    return fa1


@dataclass
class FakeArticleView:
    name: str = 'Fake Article View'


@pytest.fixture
def sm_registry():
    """ Provide test isolation for builtin service registry """

    class FakeServiceRegistry(dectate.App):
        service = dectate.directive(ServiceAction)
        request = dectate.directive(RequestAction)
        resource = dectate.directive(ResourceAction)
        view = dectate.directive(ViewAction)

    return FakeServiceRegistry


@pytest.fixture
def uninitialized_sm(sm_config, sm_registry) -> ServiceManager:
    """ Make a ServiceManager """

    sm = ServiceManager(sm_config, sm_registry)
    sm.registry = sm_registry
    return sm


@pytest.fixture
def register_service(sm_registry):
    sm_registry.service(name='request')(RequestService)
    sm_registry.service(name='resource')(ResourceService)
    sm_registry.service(name='view')(ViewService)


@pytest.fixture
def initialized_sm(uninitialized_sm, register_service, registrations):
    """ The equivalent of an app with commit """
    uninitialized_sm.initialize()
    return uninitialized_sm


@pytest.fixture
def services(initialized_sm):
    return initialized_sm.services


@pytest.fixture
def requestservice(services) -> RequestService:
    return services['request']


@pytest.fixture
def resourceservice(services) -> ResourceService:
    return services['resource']


@pytest.fixture
def viewservice(services) -> ViewService:
    return services['view']


@pytest.fixture
def fakearticle_view(sm_registry):
    sm_registry.view(for_=IndexView, resource=FakeArticle)(
        FakeArticleView)
