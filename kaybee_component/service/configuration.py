"""

Provide a pydantic model to do validated configuration on the
service manager.

"""
from typing import Mapping, Any

from pydantic import BaseModel


class ServiceManagerConfig(BaseModel):
    debug: bool = True
    serviceconfigs: Mapping[str, Any] = {}
