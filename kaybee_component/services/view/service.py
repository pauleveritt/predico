from dataclasses import dataclass

from kaybee_component.field_types import injectedattr
from kaybee_component.registry import Registry
from kaybee_component.service.base_service import BaseService
from kaybee_component.service.configuration import ServiceManagerConfig
from kaybee_component.services.view.action import ViewAction
from kaybee_component.services.view.base_view import IndexView
from kaybee_component.services.view.config import ViewServiceConfig


@dataclass(frozen=True)
class ViewService(BaseService):
    action: ViewAction
    app_registry: Registry
    config: ViewServiceConfig

    def get_view(self, app_registry):
        view_class = self.action.get_class(app_registry, for_=IndexView)
        view_instance = view_class()
        return view_instance


def setup(registry: Registry):
    registry.service(name='view')(ViewService)
