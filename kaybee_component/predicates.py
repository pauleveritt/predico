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
        return f'{self.key}-{self.value.__name__}'


@dataclass
class ForPredicate(Predicate):
    key: str = 'for_'

    def matches(self, target: IndexView) -> bool:
        # target and self.value are both classes. Are they the same?
        return target is self.value


@dataclass
class ResourcePredicate(Predicate):
    value: Type[Resource]
    key: str = 'resource'

    def matches(self, target: Resource) -> bool:
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

    def matches(self, target: str) -> bool:
        # We are given an resourceid. Look first at
        return target == self.value
