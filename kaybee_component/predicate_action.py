from typing import Sequence

import dectate


class UnknownArgument(Exception):
    fmt = 'Decorator supplied unknown predicate: {name}'


class MissingArgument(Exception):
    fmt = '__init__() missing 1 required positional argument: {name}'

class LookupMissingRequired(Exception):
    fmt ='Lookup is missing required field: {name}'

class UnknownLookup(Exception):
    fmt = 'Lookup supplied unknown predicate argument: {name}'


def _predicate_matches_lookup(predicate, lookup_args) -> bool:
    # Make sure the lookup args actually have this predicate's key
    lookup_value = lookup_args.get(predicate.key, False)
    return lookup_value and predicate.matches(lookup_value)


class PredicateAction(dectate.Action):
    config = {
        'plugins': dict
    }

    def __init__(self, **args):
        super().__init__()
        self.predicates = {}

        # Fail if we are supplied a predicate that we don't define
        defined_predicate_keys = [
            predicate.key
            for predicate in self.OPTIONAL_PREDICATES + \
                             self.REQUIRED_PREDICATES
        ]
        for argument_name in args.keys():
            if argument_name not in defined_predicate_keys:
                m = UnknownArgument.fmt.format(name=argument_name)
                raise UnknownArgument(m)

        for predicate_choice in self.REQUIRED_PREDICATES:
            key = predicate_choice.key
            if key not in args:
                m = MissingArgument.fmt.format(name=key)
                raise MissingArgument(m)
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

    @classmethod
    def sorted_actions(cls, action_name, app: dectate.App) -> Sequence[
        dectate.Action]:
        q = dectate.Query(action_name)
        sorted_actions = sorted(q(app), reverse=True)
        return sorted_actions

    def all_predicates_match(self, **args):
        """ See if match on all this registered action's predicates"""

        # Let's do this in phases, eliminating the least-cost things first.
        # We start by making some sets for keys
        required_keys = {p.key for p in self.REQUIRED_PREDICATES}
        optional_keys = {p.key for p in self.OPTIONAL_PREDICATES}
        all_keys = required_keys | optional_keys
        arg_keys = set(args.keys())

        # Phase 1: Missing required arguments
        # You can't do a lookup without a 'for_', for example, this
        # should fail with a custom exception:
        # >>> get_view(resource=Article)
        # TODO: Later find a way to let the ViewAction subclass say
        # that for_ defaults to IndexView.
        missing_required = required_keys - arg_keys
        if missing_required:
            mr = ', '.join(missing_required)
            m = LookupMissingRequired.fmt.format(name=mr)
            raise LookupMissingRequired(m)

        # Phase 2: Argument not in predicate
        # If the lookup asks for a predicate that isn't known to
        # ViewAction, raise an error
        unknown_predicate = arg_keys - all_keys
        if unknown_predicate:
            mr = ', '.join(unknown_predicate)
            m = UnknownLookup.fmt.format(name=mr)
            raise UnknownLookup(m)

        # TODO do less computation at runtime, move some to instance
        for predicate in self.predicates.values():
            is_match = _predicate_matches_lookup(predicate, args)
            if not is_match:
                # Bail out immediately
                return False
        return True

    @classmethod
    def get_class(cls, registry, action_name, **args):
        """ Look through all the actions, return best """

        sorted_actions = cls.sorted_actions(action_name, registry)

        # Find the first action which matches the args
        for action, target in sorted_actions:
            if action.all_predicates_match(**args):
                return target

        return None

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
