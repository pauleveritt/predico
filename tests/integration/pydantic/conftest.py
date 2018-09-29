import pydantic
import pytest

from predico.field_types import injectedattr
from predico.services.resource.base_resource import Resource
from predico.services.view.base_view import IndexView
from predico.services.view.config import ViewServiceConfig


@pydantic.dataclasses.dataclass
class TestPydanticArticle(Resource):
    title: str
    parentid: str

    @property
    def parentids(self):
        return [self.parentid]


@pydantic.dataclasses.dataclass
class TestPydanticSection(Resource):
    title: str
    parentid: str

    @property
    def parentids(self):
        return [self.parentid]


@pydantic.dataclasses.dataclass
class FakePydanticAdapter:
    name: str = 'Fake Pydantic Adapter'


@pydantic.dataclasses.dataclass
class TestPydanticView:
    breadcrumbs_resources: str = injectedattr(FakePydanticAdapter, 'name')
    injected_resource_title: str = injectedattr(Resource, 'title')

    viewservice_config: ViewServiceConfig
    name: str = 'One Pydantic View'


@pytest.fixture
def registrations(test_registry):
    # Resources
    test_registry.resource('testarticle')(TestPydanticArticle)
    test_registry.resource('testsection')(TestPydanticSection)

    # Views
    test_registry.view(for_=IndexView, resourceid='pydantic/about')(
        TestPydanticView)

    # Adapters
    test_registry.adapter(
        for_=FakePydanticAdapter,
    )(FakePydanticAdapter)
