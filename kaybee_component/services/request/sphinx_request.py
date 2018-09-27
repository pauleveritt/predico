from collections import UserDict
from dataclasses import dataclass
from typing import Any, Type

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
        viewservice: ViewService = services['view']
        viewinstance = viewservice.get_view(
            self,
            for_=IndexView,
        )
        return viewinstance

    @property
    def views(self):
        """ Return a closure dict that can look up a view """

        # We pack things up into a dict-like instance which
        # has access to the view service and the request.
        class ViewsGetter:
            def __init__(self, viewservice: ViewService,
                         request: SphinxRequest):
                self.viewservice = viewservice
                self.request = request

            def __getitem__(self, viewclass: Type[Any]):
                viewinstance = self.viewservice.get_view(
                    self.request,
                    for_=IndexView,
                )
                return viewinstance

        viewservice: ViewService = self.sm.services['view']
        viewsgetter = ViewsGetter(viewservice, self)
        return viewsgetter
