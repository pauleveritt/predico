from dataclasses import dataclass

from predico import registry
from predico.registry import Registry
from predico.servicemanager.base_service import BaseService
from predico.servicemanager.manager import ServiceManager
from predico.services.request.base_request import Request
from predico.services.request.common_request import CommonRequest
from predico.services.request.config import RequestServiceConfig


@registry.service(name='request')
@dataclass(frozen=True)
class RequestService(BaseService):
    sm: ServiceManager
    registry: Registry
    config: RequestServiceConfig

    def make_request(self, resourceid: str, **kwargs):
        request_class: Request = self.config.factory
        return request_class(
            sm=self.sm,
            registry=self.registry,
            resourceid=resourceid,
            **kwargs
        )
