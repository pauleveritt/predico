from dataclasses import dataclass

from predico import registry
from predico.sample import servicemanager, setup, Article
from predico.services.request.base_request import Request
from predico.services.view.base_view import View


@registry.view(
    resource=Article,
    template_string='<h1>{name}: {request.resource.title}</h1>'
)
@dataclass
class ArticleView(View):
    request: Request
    name: str = 'Article View'


if __name__ == '__main__':
    setup()
    request_service = servicemanager.services['request']
    request = request_service.make_request('more/index')
    output = request.render()
    print(output)
