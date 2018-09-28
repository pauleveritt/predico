import pydantic
import pytest

from kaybee_component.field_types import injectedattr
from kaybee_component.registry import Registry
from kaybee_component.services.request.base_request import Request
from kaybee_component.services.resource.base_resource import Resource
from kaybee_component.services.view.base_view import IndexView
from kaybee_component.services.view.config import ViewServiceConfig


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
class TestPydanticView:
    resource_title: str = injectedattr(Resource, 'title')
    viewservice_config: ViewServiceConfig
    name: str = 'One Pydantic View'


@pytest.fixture
def registrations(test_registry):
    # Resources
    test_registry.resource('testarticle')(TestPydanticArticle)
    test_registry.resource('testsection')(TestPydanticSection)
    test_registry.view(for_=IndexView, resourceid='pydantic/about')(
        TestPydanticView)
