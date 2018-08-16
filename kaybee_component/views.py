from typing import Type, Sequence, Optional

import dectate

from kaybee_component.predicates import ForPredicate, ResourcePredicate
from kaybee_component.resources import Resource
from kaybee_component.viewtypes import IndexView


class ViewForPredicate(ForPredicate):
    value: Type[IndexView]


class ViewAction(dectate.Action):
    config = {
        'plugins': dict
    }

    app_class_arg = True

    def __init__(self,
                 for_: Type[IndexView],
                 resource: Type[Resource] = None,
                 ):
        super().__init__()
        self.for_ = ViewForPredicate(value=for_)
        self.name = f'{self.for_}'
        self.sort_order = self.for_.rank

        # Now start going through each optional predicate and
        # adjusting this action's state.
        if resource:
            self.resource = ResourcePredicate(value=resource)
            self.name += f'--{self.resource}'
            self.sort_order += self.resource.rank

    def identifier(self, plugins, app_class=None):
        return self.name

    def perform(self, obj, plugins=None, app_class=None):
        if plugins is None:
            plugins = []
        plugins[self.name] = obj

    @classmethod
    def sorted_actions(cls, app: dectate.App) -> Sequence[dectate.Action]:
        q = dectate.Query('view')
        sorted_actions = sorted(q(app),
                                key=lambda x: x[0].sort_order,
                                reverse=True)
        return sorted_actions

    @classmethod
    def get_class(cls,
                  app: dectate.App,
                  for_target: Optional[IndexView] = None,
                  resource_target: Optional[Resource] = None,
                  ):
        sorted_actions = cls.sorted_actions(app)
        for action, view_class in sorted_actions:
            #
            # TODO
            # Change this. Instead of choosing based on what was passed
            # in, choose based on what the action is asking for. This
            # means:
            # - Store the action's predicates in self.predicates
            # - Sniff at predicate's .match() args to see what it wants
            if resource_target:
                # Does this action have a resource predicate?
                action_resource: ResourcePredicate = getattr(action,
                                                             'resource', False)
                if action_resource and action_resource.matches(
                        resource_target):
                    return view_class
                else:
                    # We asked for it, but it didn't match, on to the
                    # next action
                    continue

            if for_target:
                # Does this action have a for_ predicate?
                action_for: ForPredicate = getattr(action,
                                                   'for_', False)
                if action_for and action_for.matches(for_target):
                    return view_class
