from dataclasses import dataclass
from typing import Dict

from predico import registry
from predico.field_types import injected
from predico.sample import servicemanager, setup, Article, SampleResource
from predico.servicemanager.manager import ServiceManager
from predico.services.request.base_request import Request
from predico.services.resource.base_resource import Resource
from predico.services.view.base_view import View


@registry.view(
    resource=Article,
    template_string='''\
<span>{breadcrumbs}</span><h1>{name}: {resource_title}</h1>'''
)
@dataclass
class ArticleView(View):
    resources: Dict[str, SampleResource] = injected(Request, attr='resources')
    resourceid: str = injected(Resource, attr='id')
    resource_title: str = injected(Resource, attr='title')
    name: str = 'Article View'

    @property
    def breadcrumbs(self):
        titles = []
        targetid = self.resourceid
        while targetid:
            resource = self.resources[targetid]
            titles.insert(0, resource.title)
            targetid = resource.parentid

        return ' >> '.join(titles)


if __name__ == '__main__':
    setup()
    request_service = servicemanager.services['request']
    request = request_service.make_request('more/contact')
    output = request.render()
    print(output)
