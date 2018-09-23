from dataclasses import dataclass

from kaybee_component import registry
from kaybee_component.registry import Registry
from kaybee_component.service.base_service import BaseService
from kaybee_component.services.view.config import ViewServiceConfig


@registry.service(name='view')
@dataclass(frozen=True)
class ViewService(BaseService):
    app_registry: Registry
    config: ViewServiceConfig

    def get_view(self, app_registry):
        # view_class = self.action.get_class(app_registry, for_=IndexView)
        # view_instance = view_class()
        # return view_instance
        pass
