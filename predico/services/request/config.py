"""

Provide a pydantic model to do validated configuration on the
request service.

"""

from pydantic import BaseModel


class RequestServiceConfig(BaseModel):
    flag: int