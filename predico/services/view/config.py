"""

Provide a pydantic model to do validated configuration on the
view service.

"""

from pydantic import BaseModel


class ViewServiceConfig(BaseModel):
    flag: int