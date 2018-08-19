import dectate

from kaybee_component.views import ViewAction


class Kaybee(dectate.App):
    view = dectate.directive(ViewAction)
