from dataclasses import dataclass

from predico import registry
from predico.sample import servicemanager, setup, Article
from predico.services.view.base_view import View


@registry.view(
    resource=Article,
    template_string='<h1>{name}</h1>'
)
@dataclass
class ArticleView(View):
    name: str = 'Article View'


if __name__ == '__main__':
    setup()
    output = servicemanager.render('more/contact')
    print(output)

