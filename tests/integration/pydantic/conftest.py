import pydantic
import pytest

from predico.field_types import injected
from predico.services.adapter.base_adapter import Adapter
from predico.services.resource.base_resource import Resource
from predico.services.view.base_view import IndexView, View
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
class FakePydanticAdapter(Adapter):
    name: str = 'Fake Pydantic Adapter'


@pydantic.dataclasses.dataclass
class FakePydanticCallableAdapter(Adapter):
    name: str = 'Fake Pydantic Adapter'

    def __call__(self):
        return 'Result from __call__'

    @classmethod
    def validate(cls, v):
        return v

    @classmethod
    def get_validators(cls):
        yield cls.validate


@pydantic.dataclasses.dataclass
class TestPydanticView(View):
    breadcrumbs_resources: str = injected(FakePydanticAdapter, attr='name')
    callable: FakePydanticCallableAdapter
    injected_resource_title: str = injected(Resource, attr='title')

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
    test_registry.adapter(
        for_=FakePydanticCallableAdapter,
    )(FakePydanticCallableAdapter)
