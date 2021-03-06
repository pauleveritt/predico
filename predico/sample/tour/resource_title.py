from dataclasses import dataclass

from predico import registry
from predico.field_types import injected
from predico.sample import servicemanager, setup, Article
from predico.services.resource.base_resource import Resource


@registry.view(
    resource=Article,
    template_string='<h1>{v.name}: {v.resource_title}</h1>'
)
@dataclass
class ArticleView:
    resource_title: str = injected(Resource, attr='title')
    name: str = 'Article View'


if __name__ == '__main__':
    setup()
    request_service = servicemanager.services['request']
    request = request_service.make_request('more/index')
    output = request.render()
    print(output)
