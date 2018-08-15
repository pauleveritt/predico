from dataclasses import dataclass
from typing import Type, Any

from kaybee_component.resources import Resource


@dataclass
class ForPredicate:
    value: Type[Any]
    key: str = 'for_'
    rank: int = 10

    def __str__(self):
        return f'for_-{self.value.__name__}'


@dataclass
class ResourcePredicate:
    value: Type[Resource]
    key: str = 'resource'
    rank: int = 10

    def __str__(self):
        return f'resource-{self.value.__name__}'
