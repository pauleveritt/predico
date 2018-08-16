from dataclasses import dataclass
from typing import Type, Any

from kaybee_component.resources import Resource
from kaybee_component.viewtypes import IndexView


@dataclass
class ForPredicate:
    value: Type[Any]
    key: str = 'for_'
    rank: int = 10

    def __str__(self):
        return f'for_-{self.value.__name__}'

    def matches(self, target: IndexView) -> bool:
        return target == self.value


@dataclass
class ResourcePredicate:
    value: Type[Resource]
    key: str = 'resource'
    rank: int = 10

    def __str__(self):
        return f'resource-{self.value.__name__}'

    def matches(self, target: Resource) -> bool:
        return self.value == target
