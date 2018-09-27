from typing import Sequence, List, Any

import dectate

from kaybee_component.predicates import Predicate
from kaybee_component.services.request.base_request import Request


class UnknownArgument(Exception):
    fmt = 'Decorator supplied unknown predicate: {name}'


class MissingArgument(Exception):
    fmt = '__init__() missing 1 required positional argument: {name}'


class LookupMissingRequired(Exception):
    fmt = 'Lookup is missing required field: {name}'


class UnknownLookup(Exception):
    fmt = 'Lookup supplied unknown predicate argument: {name}'


def reject_predicates(
        required: List[Predicate],
        optional: List[Predicate],
        **kwargs
):
    """ Given requried and optional predicates, do a sanity check """

    # Let's do this in phases, eliminating the least-cost things first.
    # We start by making some sets for keys
    required_keys = {p.key for p in required}
    optional_keys = {p.key for p in optional}
    all_keys = required_keys | optional_keys
    arg_keys = set(kwargs.keys())

    # Phase 1: Missing required arguments
    # You can't do a lookup without a 'for_', for example, this
    # should fail with a custom exception.
    # >>> get_view(resource=Article)
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


def predicates_match(
        request: Request,
        predicate_values: List[Any],
        **kwargs):
    """ Given a group of predicates, return False if any don't match """
    for predicate in predicate_values:
        is_match = predicate.matches(request, **kwargs)
        if not is_match:
            # Bail out immediately
            return False
    return True


class PredicateAction(dectate.Action):
    config = {
        'plugins': dict
    }

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.predicates = {}

        # Fail if we are supplied a predicate that we don't define
        defined_predicate_keys = [
            predicate.key
            for predicate in
            self.OPTIONAL_PREDICATES + self.REQUIRED_PREDICATES
        ]
        for argument_name in kwargs.keys():
            if argument_name not in defined_predicate_keys:
                m = UnknownArgument.fmt.format(name=argument_name)
                raise UnknownArgument(m)

        for predicate_choice in self.REQUIRED_PREDICATES:
            key = predicate_choice.key
            if key not in kwargs:
                m = MissingArgument.fmt.format(name=key)
                raise MissingArgument(m)
            predicate = predicate_choice(value=kwargs[key])
            self.predicates[key] = predicate

        for predicate_choice in self.OPTIONAL_PREDICATES:
            key = predicate_choice.key
            if key in kwargs:
                predicate = predicate_choice(value=kwargs[key])
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
    def sorted_actions(cls,
                       registry: dectate.App
                       ) -> Sequence[dectate.Action]:
        # TODO Move this to BaseService constructor to avoid calculating
        # up each time. Then refactor ViewService etc. tests to not
        # need a registry by mocking sorted_actions.
        q = dectate.Query(cls.action_name)
        actions = list(q(registry))
        sorted_actions = sorted(actions, reverse=True,
                                key=lambda x: x[0])
        return sorted_actions

    def all_predicates_match(self, request, **kwargs):
        """ See if match on all this registered action's predicates"""

        # For performance and sanity check, raise some exceptions
        # if stuff is missing, undefined, etc.
        reject_predicates(
            self.REQUIRED_PREDICATES,
            self.OPTIONAL_PREDICATES,
            **kwargs
        )

        # Go through each predicate on this action instance/registration
        # and see if the incoming data "matches"
        for predicate in self.predicates.values():
            is_match = predicate.matches(request, **kwargs)
            if not is_match:
                # Bail out immediately
                return False

        return True

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
