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

    def get_resourceclass(self, rtype: str):
        """ Given name a resource type was registered with, get class """

        return Resource

    def get_resource(self, resourceid: str):
        resource = self.resources[resourceid]

        return resource

    def add_resource(self, **kwargs):
        """ Pass in dict of values and let the service construct/store """

        # Resources don't participate in DI so just construct them
        rtype = kwargs['rtype']
        resourceclass = self.get_resourceclass(rtype)
        resource = Resource(**kwargs)
        resourceid = resource.id
        self.resources[resourceid] = resource
        return resource