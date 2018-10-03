"""

The ResourceService. Stores, retrieves, and updates resources.

"""

from dataclasses import dataclass, field
from typing import Dict

from predico import registry
from predico.registry import Registry
from predico.servicemanager.base_service import BaseService
from predico.servicemanager.manager import ServiceManager
from predico.services.resource.base_resource import Resource, Resources
from predico.services.resource.config import ResourceServiceConfig


@registry.service(name='resource')
@dataclass(frozen=True)
class ResourceService(BaseService):
    sm: ServiceManager
    registry: Registry
    config: ResourceServiceConfig
    resources: Resources = field(default_factory=Resources)

    def get_resourceclass(self, rtype: str):
        """ Given name a resource type was registered with, get class """

        resource_classes = self.registry.config.resources
        resource_class = resource_classes[rtype]
        return resource_class

    def get_resource(self, resourceid: str) -> Resource:
        resource = self.resources[resourceid]

        return resource

    def add_resource(self, **kwargs) -> Resource:
        """ Pass in dict of values and let the service construct/store """

        # Resources don't participate in DI so just construct them
        rtype = kwargs['rtype']
        resourceclass = self.get_resourceclass(rtype)
        resource = resourceclass(**kwargs)
        resourceid = resource.id
        self.resources[resourceid] = resource
        return resource
