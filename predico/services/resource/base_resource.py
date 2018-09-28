# Fake resource
from dataclasses import dataclass


@dataclass
class Resource:
    rtype: str
    id: str
