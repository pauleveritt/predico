from dataclasses import dataclass
from typing import Sequence, Any

from kaybee_component.field_types import injected, injectedattr
from kaybee_component.registry import PredicateRegistry
from kaybee_component.service.base_service import BaseService
from kaybee_component.service.configuration import ServiceManagerConfig
from kaybee_component.service.registry import services
from kaybee_component.services.view.action import ViewAction
from kaybee_component.services.view.base_view import IndexView
from kaybee_component.services.view.config import ViewServiceConfig


@dataclass(frozen=True)
class ViewService(BaseService):
    action: ViewAction = injected()
    app_registry: PredicateRegistry = injected()
    config: ViewServiceConfig = injected()
    allconfigs: Sequence[Any] = injectedattr(ServiceManagerConfig,
                                             'serviceconfigs')

    def get_view(self, app_registry):
        view_class = self.action.get_class(app_registry, 'view',
                                           for_=IndexView)
        view_instance = view_class()
        return view_instance


def setup(registry: services):
    registry.service(name='view')(ViewService)
