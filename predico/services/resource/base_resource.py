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
