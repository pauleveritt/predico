from dataclasses import dataclass

from kaybee_component.field_types import injected
from kaybee_component.service.base_service import BaseService
from kaybee_component.services.request.config import RequestServiceConfig
from kaybee_component.services.request.registry import RequestRegistry


@dataclass(frozen=True)
class RequestService(BaseService):
    config: RequestServiceConfig = injected()
    registry: RequestRegistry = RequestRegistry
