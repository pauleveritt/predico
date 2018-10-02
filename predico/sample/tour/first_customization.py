from dataclasses import dataclass

from predico import registry
from predico.sample import servicemanager, setup, Article


@registry.view(
    resource=Article,
    template_string='<h1>{v.name}</h1>'
)
@dataclass
class ArticleView:
    name: str = 'Article View'


if __name__ == '__main__':
    setup()
    output = servicemanager.render('more/contact')
    print(output)
