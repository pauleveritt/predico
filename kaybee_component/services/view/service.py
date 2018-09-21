from dataclasses import dataclass
from typing import Sequence, Any

from kaybee_component.field_types import injected, injectedattr
from kaybee_component.service.base_service import BaseService
from kaybee_component.service.configuration import ServiceManagerConfig
from kaybee_component.service.registry import services
from kaybee_component.services.view.config import ViewServiceConfig


@dataclass(frozen=True)
class ViewService(BaseService):
    config: ViewServiceConfig = injected()
    allconfigs: Sequence[Any] = injectedattr(ServiceManagerConfig,
                                             'serviceconfigs')


def setup(registry: services):
    registry.service(name='view')(ViewService)
