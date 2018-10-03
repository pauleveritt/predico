# Fake resource
from dataclasses import dataclass


@dataclass
class Resource:
    rtype: str
    id: str


class Resources(dict):
    """

    Custom dictionary container for storing resources.

    This was first created because we needed a marker to make
    Resources an injectable. Later we might do some things like
    caching.

    """

    pass
