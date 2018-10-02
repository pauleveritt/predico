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


@registry.view(
    resourceid='more/specificid',
    template_string='<h1>{v.name}</h1>'
)
@dataclass
class SpecificArticleView:
    name: str = 'Specific Article View'


if __name__ == '__main__':
    setup()
    output = servicemanager.render('more/specificid')
    print(output)
