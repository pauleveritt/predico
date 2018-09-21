import dectate

from kaybee_component.services.request.action import RequestAction
from kaybee_component.services.view.action import ViewAction


class PredicoApp(dectate.App):
    view = dectate.directive(ViewAction)
    request = dectate.directive(RequestAction)
