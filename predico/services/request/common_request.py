import dataclasses
from dataclasses import dataclass
from typing import Any, Type

from predico.registry import Registry
from predico.servicemanager.manager import ServiceManager
from predico.services.adapter.service import AdapterService
from predico.services.request.base_request import Request
from predico.services.resource.base_resource import Resource
from predico.services.resource.service import ResourceService
from predico.services.view.renderers import StringFormatRenderer
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
    def resources(self):
        """ Return the resource service's resources """
        services = self.sm.services
        rs: ResourceService = services['resource']
        resources = rs.resources
        return resources

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

    def adapt_resource(self, for_: Type[Any], resource: Resource):
        """ Instead of using request.resource implictly, use passed-in """

        adapterservice: AdapterService = self.sm.services['adapter']

        adapterinstance = adapterservice.get_adapter(
            self,
            for_=for_,
            resource=resource
        )
        return adapterinstance

    def render(self) -> str:
        """ Use the view and the render/template """

        services = self.sm.services
        viewservice: ViewService = services['view']

        # Get the current view instance
        viewinstance = viewservice.get_view(self)

        # Get the view *action* to find out renderer/template information
        viewaction = viewservice.get_viewaction(self)

        # Find the renderer, if none, use StringFormatRenderer
        nlp = viewaction.nonlookup_predicates
        renderer_adapter_class = nlp.get('renderer', StringFormatRenderer)
        renderer_adapter = self.adapters[renderer_adapter_class]
        if renderer_adapter is None:
            # No adapter, just use the default implementation
            renderer_adapter = renderer_adapter_class

        template_string_predicate = nlp.get('template_string', None)
        if template_string_predicate:
            template_string = template_string_predicate.value
            renderer = renderer_adapter(template_string=template_string,
                                        view=viewinstance)

            # Render in the context of the view
            output = renderer()
            return output
