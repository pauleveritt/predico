from dataclasses import field, dataclass
from typing import List

import dectate
import pytest

from predico.servicemanager.action import ServiceAction
from predico.servicemanager.manager import ServiceManager
from predico.services.adapter.action import AdapterAction
from predico.services.adapter.base_adapter import Adapter
from predico.services.adapter.service import AdapterService
from predico.services.request.action import RequestAction
from predico.services.request.service import RequestService
from predico.services.resource.action import ResourceAction
from predico.services.resource.base_resource import Resource
from predico.services.resource.service import ResourceService
from predico.services.view.action import ViewAction
from predico.services.view.base_view import View
from predico.services.view.service import ViewService


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
    fa2 = FakeArticle(id='more/article2', parentids=['more/index', 'index'])
    return fa2


@dataclass
class FakeArticleView(View):
    name: str = 'Fake Article View'


@dataclass
class FakeTemplateStringView(View):
    name: str = 'Fake Template String View'


@dataclass
class FakeBreadcrumbsResources:
    """ Something we want as the result of adaptation """

    pass


@dataclass
class FakeBreadcrumbsResourcesAdapter(Adapter):
    resource: Resource
    name: str = 'Fake Breadcrumbs Resources'

    def __call__(self):
        return self


@pytest.fixture
def fake_breadcrumbs_resources():
    return FakeBreadcrumbsResources


@dataclass
class FakeArticleAdapter(Adapter):
    name: str = 'Fake Article Adapter'


@pytest.fixture
def sm_registry():
    """ Provide test isolation for builtin service registry """

    class FakeServiceRegistry(dectate.App):
        adapter = dectate.directive(AdapterAction)
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
    sm_registry.service(name='adapter')(AdapterService)
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
    sm_registry.view(resource=FakeArticle)(FakeArticleView)


@pytest.fixture
def fake_templatestring_view(sm_registry):
    sm_registry.view(
        resourceid='more/article1',
        template_string='<p>View Name: {v.name}</p>')(FakeTemplateStringView)


@pytest.fixture
def fakearticle_adapter(sm_registry):
    sm_registry.adapter(
        for_=FakeBreadcrumbsResources,
        resource=FakeArticle)(FakeBreadcrumbsResourcesAdapter)
