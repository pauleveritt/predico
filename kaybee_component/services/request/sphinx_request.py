from dataclasses import dataclass

from kaybee_component.registry import Registry
from kaybee_component.service.manager import ServiceManager
from kaybee_component.services.resource.service import ResourceService
from kaybee_component.services.view.service import ViewService


@dataclass(frozen=True)
class SphinxRequest:
    resourceid: str
    sm: ServiceManager
    app_registry: Registry

    @property
    def resource(self):
        """ Given information in request, get the current resource """
        return 9912

    @property
    def view(self):
        """ Given information in request, find best-match view """

        services = self.sm.services
        view_service: ViewService = services['view']
        return view_service.get_view(self.app_registry)
