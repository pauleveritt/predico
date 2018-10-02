from dataclasses import dataclass
from typing import Dict, List

from predico import registry
from predico.field_types import injected
from predico.sample import servicemanager, setup, Article, SampleResource
from predico.services.request.base_request import Request
from predico.services.resource.base_resource import Resource


class Breadcrumbs:
    pass


@registry.adapter(for_=Breadcrumbs)
@dataclass
class BreadcrumbsAdapter:
    resources: Dict[str, SampleResource] = injected(Request, attr='resources')
    resourceid: str = injected(Resource, attr='id')

    def __call__(self) -> List[SampleResource]:
        resources = []
        targetid = self.resourceid
        while targetid is not None:
            resource = self.resources[targetid]
            resources.insert(0, resource)
            targetid = resource.parentid

        return resources


@registry.view(
    resource=Article,
    template_string='''\
<span>{v.breadcrumb_titles}</span>
<h1>{v.name}: {v.resource_title}</h1>'''
)
@dataclass
class ArticleView:
    breadcrumbs: Breadcrumbs
    resource_title: str = injected(Resource, attr='title')
    name: str = 'Article View'

    @property
    def breadcrumb_titles(self):
        return ' >> '.join([r.title for r in self.breadcrumbs])


if __name__ == '__main__':
    setup()
    request_service = servicemanager.services['request']
    request = request_service.make_request('more/contact')
    output = request.render()
    print(output)
