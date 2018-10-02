"""

Provide a pydantic model to do validated configuration on the
request service.

"""

import pydantic

from predico.services.request.base_request import Request
from predico.services.request.common_request import CommonRequest


@pydantic.dataclasses.dataclass
class RequestServiceConfig:
    flag: int
    factory: Request = CommonRequest
