from dataclasses import dataclass

from kaybee_component.field_types import injected
from kaybee_component.registry import PredicoRegistry
from kaybee_component.service.base_service import BaseService
from kaybee_component.service.manager import ServiceManager
from kaybee_component.service.registry import services
from kaybee_component.services.request.config import RequestServiceConfig
from kaybee_component.services.view.service import ViewService


@dataclass(frozen=True)
class SphinxRequest:
    resource_id: str
    sm: ServiceManager
    app_registry: PredicoRegistry

    @property
    def view(self):
        """ Given information in request, find best-match view """

        services = self.sm.services
        view_service: ViewService = services['view']
        return view_service.get_view(self.app_registry)


@dataclass(frozen=True)
class RequestService(BaseService):
    config: RequestServiceConfig = injected()

    def make_request(self, **kwargs):
        return SphinxRequest(**kwargs)


def setup(registry: services):
    registry.service(name='request')(RequestService)
