from dataclasses import dataclass

from kaybee_component.registry import Registry
from kaybee_component.servicemanager.manager import ServiceManager
from kaybee_component.services.view.base_view import IndexView
from kaybee_component.services.view.service import ViewService


@dataclass(frozen=True)
class SphinxRequest:
    resourceid: str
    sm: ServiceManager
    registry: Registry

    @property
    def resource(self):
        """ Given information in request, get the current resource """
        services = self.sm.services
        rs = services['resource']
        resource = rs.get_resource(self.resourceid)
        return resource

    @property
    def view(self):
        """ Given information in request, find best-match view """

        services = self.sm.services
        view_service: ViewService = services['view']
        return view_service.get_view(
            self,
            for_=IndexView,
        )
