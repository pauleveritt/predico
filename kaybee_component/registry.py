import dectate

from kaybee_component.services.request.action import RequestAction
from kaybee_component.services.view.action import ViewAction


class PredicoRegistry(dectate.App):
    """ A fully-assembled registry """
    view = dectate.directive(ViewAction)
    request = dectate.directive(RequestAction)

