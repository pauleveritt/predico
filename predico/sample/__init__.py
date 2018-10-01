"""

Sample used for documentation and full testing.

Contains a service manager with some views, resources, and adapters.

"""
from dataclasses import dataclass
from typing import Optional

from predico import registry
from predico.field_types import injected
from predico.servicemanager.configuration import ServiceManagerConfig
from predico.servicemanager.manager import ServiceManager
from predico.services.adapter.config import AdapterServiceConfig
from predico.services.request.config import RequestServiceConfig
from predico.services.resource.base_resource import Resource
from predico.services.resource.config import ResourceServiceConfig
from predico.services.resource.service import ResourceService
from predico.services.view.base_view import View
from predico.services.view.config import ViewServiceConfig


@dataclass
class SampleResource:
    id: str
    title: str
    parentid: Optional[str] = None


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


config = ServiceManagerConfig(serviceconfigs=dict(
    adapterservice=AdapterServiceConfig(flag=1),
    resourceservice=ResourceServiceConfig(flag=1),
    requestservice=RequestServiceConfig(flag=1),
    viewservice=ViewServiceConfig(flag=1),

))
servicemanager = ServiceManager(config, registry)


def setup():
    servicemanager.initialize()

    # Add some resources
    rs: ResourceService = servicemanager.services['resource']
    rs.add_resource(rtype='section', id='index', title='Home Page')
    rs.add_resource(rtype='section', id='more/index',
                    title='More Section', parentid='more/index')
    rs.add_resource(rtype='article', id='more/contact',
                    title='Contact', parentid='more/index')
    rs.add_resource(rtype='article', id='more/specificid',
                    title='Specific', parentid='more/index')
    rs.add_resource(rtype='article', id='news/first',
                    title='Contact', parentid='news/index')


if __name__ == '__main__':
    setup()
    output = servicemanager.render('more/index')
    assert '<h1>Resource View: More Section</h1>' == output
    print(output)
