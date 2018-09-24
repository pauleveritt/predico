"""

The ResourceService. Stores, retrieves, and updates resources.

"""

from dataclasses import dataclass, field
from typing import Dict

from kaybee_component import registry
from kaybee_component.registry import Registry
from kaybee_component.service.base_service import BaseService
from kaybee_component.service.manager import ServiceManager
from kaybee_component.services.resource.base_resource import Resource
from kaybee_component.services.resource.config import ResourceServiceConfig


@registry.service(name='resource')
@dataclass(frozen=True)
class ResourceService(BaseService):
    sm: ServiceManager
    app_registry: Registry
    config: ResourceServiceConfig
    resources: Dict[str, Resource] = field(default_factory=dict)

    # NEXT
    # Have a set_resource which finds the right class,
    # etc.

    def get_resource(self, resourceid: str):
        resource = self.resources[resourceid]

        return resource
