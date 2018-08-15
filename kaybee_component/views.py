from typing import Type

import dectate

from kaybee_component.predicates import ForPredicate


class IndexView:
    pass


class ViewForPredicate(ForPredicate):
    value: Type[IndexView]


class ViewAction(dectate.Action):
    name: str
    config = {
        'plugins': dict
    }

    app_class_arg = True

    def __init__(self, for_: Type[IndexView]):
        super().__init__()
        self.for_ = ViewForPredicate(for_)
        self.name = f'{self.for_}'

    def identifier(self, plugins, app_class=None):
        return self.name

    def perform(self, obj, plugins=None, app_class=None):
        if plugins is None:
            plugins = []
        plugins[self.name] = obj
