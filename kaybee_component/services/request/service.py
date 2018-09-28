from dataclasses import dataclass

from kaybee_component import registry
from kaybee_component.registry import Registry
from kaybee_component.servicemanager.base_service import BaseService
from kaybee_component.servicemanager.manager import ServiceManager
from kaybee_component.services.request.config import RequestServiceConfig
from kaybee_component.services.request.common_request import CommonRequest


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
