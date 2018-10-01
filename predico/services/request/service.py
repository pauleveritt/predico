from dataclasses import dataclass
from typing import Optional

from predico import registry
from predico.registry import Registry
from predico.servicemanager.base_service import BaseService
from predico.servicemanager.manager import ServiceManager
from predico.services.request.base_request import Request
from predico.services.request.config import RequestServiceConfig
from predico.services.request.common_request import CommonRequest


@registry.service(name='request')
@dataclass(frozen=True)
class RequestService(BaseService):
    sm: ServiceManager
    registry: Registry
    config: RequestServiceConfig

    def make_request(self, resourceid: str):
        return CommonRequest(
            sm=self.sm,
            registry=self.registry,
            resourceid=resourceid
        )
