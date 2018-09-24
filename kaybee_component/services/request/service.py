from dataclasses import dataclass

from kaybee_component import registry
from kaybee_component.registry import Registry
from kaybee_component.service.base_service import BaseService
from kaybee_component.service.manager import ServiceManager
from kaybee_component.services.request.config import RequestServiceConfig
from kaybee_component.services.request.sphinx_request import SphinxRequest


@registry.service(name='request')
@dataclass(frozen=True)
class RequestService(BaseService):
    config: RequestServiceConfig
    sm: ServiceManager
    app_registry: Registry

    def make_request(self, resourceid: str):
        return SphinxRequest(
            sm=self.sm,
            app_registry=self.app_registry,
            resourceid=resourceid
        )
