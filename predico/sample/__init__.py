"""

Sample used for documentation and full testing.

Contains a service manager with some views, resources, and adapters.

"""
from dataclasses import dataclass

from predico import registry
from predico.field_types import injected
from predico.servicemanager.configuration import ServiceManagerConfig
from predico.servicemanager.manager import ServiceManager
from predico.services.adapter.config import AdapterServiceConfig
from predico.services.request.config import RequestServiceConfig
from predico.services.request.service import RequestService
from predico.services.resource.base_resource import Resource
from predico.services.resource.config import ResourceServiceConfig
from predico.services.resource.service import ResourceService
from predico.services.view.base_view import View
from predico.services.view.config import ViewServiceConfig


@dataclass
class SampleResource:
    id: str
    parentid: str
    title: str

    @property
    def parentids(self):
        return [self.parentid]


@registry.resource('article')
@dataclass
class Article(SampleResource):
    rtype: str = 'article'


@registry.resource('section')
@dataclass
class Section(SampleResource):
    rtype: str = 'section'


@registry.view(template_string='<h1>{name}: {resource_title}</h1>')
@dataclass
class ResourceView(View):
    resource_title: str = injected(Resource, attr='title')
    name: str = 'Resource View'


def initialize():
    config = ServiceManagerConfig(serviceconfigs=dict(
        adapterservice=AdapterServiceConfig(flag=1),
        resourceservice=ResourceServiceConfig(flag=1),
        requestservice=RequestServiceConfig(flag=1),
        viewservice=ViewServiceConfig(flag=1),

    ))
    service_manager = ServiceManager(config, registry)
    service_manager.initialize()

    # Add some resources
    rs: ResourceService = service_manager.services['resource']
    rs.add_resource(rtype='section', id='more/index',
                    title='More Section', parentid='more/index')

    rs.add_resource(rtype='article', id='news/first',
                    title='Contact', parentid='news/index')

    rs.add_resource(rtype='article', id='more/contact',
                    title='Contact', parentid='more/index')

    rs.add_resource(rtype='article', id='more/specificid',
                    title='Specific', parentid='more/index')

    return service_manager


if __name__ == '__main__':
    sm = initialize()
    request_service: RequestService = sm.services['request']
    request = request_service.make_request('more/contact')
    output = request.render()
    assert '<h1>Resource View: Contact</h1>' == output
    print(output)
