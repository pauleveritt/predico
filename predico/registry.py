import dectate

from predico.servicemanager.action import ServiceAction
from predico.services.adapter.action import AdapterAction
from predico.services.request.action import RequestAction
from predico.services.resource.action import ResourceAction
from predico.services.view.action import ViewAction


class Registry(dectate.App):
    """ A fully-assembled registry """

    adapter = dectate.directive(AdapterAction)
    resource = dectate.directive(ResourceAction)
    request = dectate.directive(RequestAction)
    service = dectate.directive(ServiceAction)
    view = dectate.directive(ViewAction)
