from dataclasses import dataclass
from typing import Type

from kaybee_component.views import View


@dataclass
class ForPredicate:
    value: Type[View]
    key: str = 'for_'
