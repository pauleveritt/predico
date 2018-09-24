"""

Provide a pydantic model to do validated configuration on the
resource service.

"""

from pydantic import BaseModel


class ResourceServiceConfig(BaseModel):
    flag: int
