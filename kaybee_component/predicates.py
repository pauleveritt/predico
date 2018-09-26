from dataclasses import dataclass
from typing import Type, Any

from kaybee_component.predicate_action import PredicateAction
from kaybee_component.services.resource.base_resource import Resource
from kaybee_component.services.view.base_view import IndexView


@dataclass
class Predicate:
    action: PredicateAction
    value: Type[Any]
    key: str
    rank: int = 10

    def __str__(self):
        value = getattr(self.value, '__name__', False)
        if not value:
            value = self.value  # Hope it's a string
        return f'{self.key}-{value}'


@dataclass
class ForPredicate(Predicate):
    key: str = 'for_'

    def matches(self, target: IndexView, request=None) -> bool:
        # target and self.value are both classes. Are they the same?
        return target is self.value


@dataclass
class ResourcePredicate(Predicate):
    value: Type[Resource]
    key: str = 'resource'

    def matches(self, target: Resource, request=None) -> bool:
        # target and self.value are both classes. Are they the same?
        return target is self.value


@dataclass
class ParentSelfPredicate(Predicate):
    """ Match on the resource id of yourself or a parent """

    # This is useful when targeting a registration at a single resource,
    # or a whole group of resources in part of a tree.

    value: str
    key: str = 'parentself'
    rank: int = 20

    def matches(self, target: str, request) -> bool:
        # We are given an resourceid. Get the resource and look at
        # it's resource id, then up the parents.

        # TODO This does not work right. When there is a valid registration
        # for both a parent and a child, it will match whichever happens
        # to sort first. Child should be more precise than parent.
        # Unfortunately that could mean that self.rank has to be
        # dynamic which messes up sorted_actions being precomputed.


        return target == self.value
