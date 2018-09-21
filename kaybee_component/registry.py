import dectate

from kaybee_component.service.action import ServiceAction
from kaybee_component.services.request.action import RequestAction
from kaybee_component.services.view.action import ViewAction


class Registry(dectate.App):
    """ A fully-assembled registry """

    view = dectate.directive(ViewAction)
    request = dectate.directive(RequestAction)
    service = dectate.directive(ServiceAction)
