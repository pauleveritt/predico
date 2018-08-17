from typing import Sequence

import dectate

msg = "__init__() missing 1 required positional argument: "


class PredicateAction(dectate.Action):
    config = {
        'plugins': dict
    }

    def __init__(self, **args):
        super().__init__()
        self.predicates = {}

        for predicate_choice in self.REQUIRED_PREDICATES:
            key = predicate_choice.key
            if key not in args:
                m = msg + key
                raise TypeError(m)
            predicate = predicate_choice(value=args[key])
            self.predicates[key] = predicate

        for predicate_choice in self.OPTIONAL_PREDICATES:
            key = predicate_choice.key
            if key in args:
                predicate = predicate_choice(value=args[key])
                self.predicates[key] = predicate

        predicate_values = self.predicates.values()
        self.name = '--'.join(
            [str(predicate) for predicate in predicate_values]
        )
        self.sort_order = sum(
            [predicate.rank for predicate in predicate_values]
        )

    def __str__(self):
        return self.name

    def identifier(self, plugins):
        return self.name

    def perform(self, obj, plugins=None):
        if plugins is None:
            plugins = []
        plugins[self.name] = obj

    def __lt__(self, other):
        return self.sort_order < other.sort_order

    def __gt__(self, other):
        return self.sort_order > other.sort_order

    def __eq__(self, other):
        return self.sort_order == other.sort_order

    def __le__(self, other):
        return self.sort_order <= other.sort_order

    def __ge__(self, other):
        return self.sort_order >= other.sort_order

    @classmethod
    def sorted_actions(cls, action_name, app: dectate.App) -> Sequence[
        dectate.Action]:
        q = dectate.Query(action_name)
        sorted_actions = sorted(q(app), reverse=True)
        return sorted_actions

    @classmethod
    def get_class(cls,
                  app: dectate.App,
                  for_target=None,
                  resource_target=None,
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
                action_resource = getattr(action,
                                          'resource',
                                          False)
                if action_resource and action_resource.matches(
                        resource_target):
                    return view_class
                else:
                    # We asked for it, but it didn't match, on to the
                    # next action
                    continue

            if for_target:
                # Does this action have a for_ predicate?
                action_for = getattr(action,
                                     'for_', False)
                if action_for and action_for.matches(for_target):
                    return view_class
