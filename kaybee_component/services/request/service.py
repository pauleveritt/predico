from dataclasses import dataclass

from kaybee_component.field_types import injected
from kaybee_component.service.base_service import BaseService
from kaybee_component.services.request.config import RequestServiceConfig
from kaybee_component.services.request.registry import BaseRequestRegistry


@dataclass(frozen=True)
class RequestService(BaseService):
    registry: BaseRequestRegistry
    config: RequestServiceConfig = injected()
