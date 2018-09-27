import dectate

from kaybee_component.servicemanager.action import ServiceAction
from kaybee_component.services.adapter.action import AdapterAction
from kaybee_component.services.request.action import RequestAction
from kaybee_component.services.resource.action import ResourceAction
from kaybee_component.services.view.action import ViewAction


class Registry(dectate.App):
    """ A fully-assembled registry """

    adapter = dectate.directive(AdapterAction)
    resource = dectate.directive(ResourceAction)
    request = dectate.directive(RequestAction)
    service = dectate.directive(ServiceAction)
    view = dectate.directive(ViewAction)
