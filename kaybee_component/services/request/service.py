from dataclasses import dataclass

from kaybee_component import registry
from kaybee_component.registry import Registry
from kaybee_component.service.base_service import BaseService
from kaybee_component.service.manager import ServiceManager
from kaybee_component.services.request.config import RequestServiceConfig
from kaybee_component.services.view.service import ViewService


@dataclass(frozen=True)
class SphinxRequest:
    resource_id: str
    sm: ServiceManager
    app_registry: Registry

    @property
    def view(self):
        """ Given information in request, find best-match view """

        services = self.sm.services
        view_service: ViewService = services['view']
        return view_service.get_view(self.app_registry)


@registry.service(name='request')
@dataclass(frozen=True)
class RequestService(BaseService):
    config: RequestServiceConfig

    def make_request(self, **kwargs):
        return SphinxRequest(**kwargs)
