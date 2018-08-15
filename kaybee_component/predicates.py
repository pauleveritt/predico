from dataclasses import dataclass
from typing import Type, Any


@dataclass
class ForPredicate:
    value: Type[Any]
    key: str = 'for_'

    def __str__(self):
        return f'for_-{self.value.__name__}'
