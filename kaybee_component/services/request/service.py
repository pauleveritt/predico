from dataclasses import dataclass

from kaybee_component.field_types import injected
from kaybee_component.service.base_service import BaseService
from kaybee_component.service.registry import services
from kaybee_component.services.request.config import RequestServiceConfig


@dataclass(frozen=True)
class RequestService(BaseService):
    config: RequestServiceConfig = injected()


def setup(registry: services):
    registry.service(name='request')(RequestService)
