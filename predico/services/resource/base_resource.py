# Fake resource
from dataclasses import dataclass


@dataclass
class Resource:
    rtype: str
    id: str

    # The following make pydantic happy
    @classmethod
    def validate(cls, v):
        # do some validation or simply pass through the value
        return v

    @classmethod
    def get_validators(cls):
        yield cls.validate


class Resources(dict):
    """

    Custom dictionary container for storing resources.

    This was first created because we needed a marker to make
    Resources an injectable. Later we might do some things like
    caching.

    """

    pass
