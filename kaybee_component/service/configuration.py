"""

Provide a pydantic model to do validated configuration on the
service manager.

"""
from pydantic import BaseModel


class ServiceManagerConfig(BaseModel):
    debug: bool = True
