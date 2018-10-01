"""

Provide a pydantic model to do validated configuration on the
request service.

"""

from pydantic import BaseModel

from predico.services.request.base_request import Request
from predico.services.request.common_request import CommonRequest


class RequestServiceConfig(BaseModel):
    factory: Request = CommonRequest
