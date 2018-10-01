from dataclasses import dataclass
from typing import Any, Type

from predico.registry import Registry
from predico.servicemanager.manager import ServiceManager
from predico.services.adapter.service import AdapterService
from predico.services.request.base_request import Request
from predico.services.view.service import ViewService


@dataclass(frozen=True)
class CommonRequest(Request):
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
        viewinstance = viewservice.get_view(self)
        return viewinstance

    @property
    def adapters(self):
        """ Return a closure dict that can look up a adapter """

        # We pack things up into a dict-like instance which
        # has access to the adapter service and the request.
        class AdaptersGetter:
            def __init__(self, adapterservice: AdapterService,
                         request: CommonRequest):
                self.adapterservice = adapterservice
                self.request = request

            def __getitem__(self, adapterclass: Type[Any]):
                adapterinstance = self.adapterservice.get_adapter(
                    self.request,
                    for_=adapterclass,
                )
                return adapterinstance

        adapterservice: AdapterService = self.sm.services['adapter']
        adaptersgetter = AdaptersGetter(adapterservice, self)
        return adaptersgetter
