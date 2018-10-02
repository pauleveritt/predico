"""

A marker and base class for the minimum request.

Certain systems, like Sphinx, will one-day register a SphinxRequest to serve
in this role.

"""


class Request:
    @classmethod
    def validate(cls, v):
        return v

    @classmethod
    def get_validators(cls):
        yield cls.validate
