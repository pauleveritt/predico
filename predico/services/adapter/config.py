"""

Provide a pydantic model to do validated configuration on the
adapter service.

"""

from pydantic import BaseModel


class AdapterServiceConfig(BaseModel):
    flag: int