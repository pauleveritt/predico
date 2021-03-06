from dataclasses import dataclass
from typing import Type, Any, Optional

from predico.services.request.base_request import Request
from predico.services.resource.base_resource import Resource


@dataclass
class Predicate:
    value: Any
    key: str
    rank: int = 10

    def __str__(self):
        value = getattr(self.value, '__name__', False)
        if not value:
            value = self.value  # Hope it's a string
        return f'{self.key}-{value}'

    def matches(self, request: Request, **args) -> bool:
        raise NotImplementedError


@dataclass
class ForPredicate(Predicate):
    value: Type[Any]
    key: str = 'for_'

    def matches(self, request: Request, **args) -> bool:
        # for_ and self.value are both classes. Are they the same?
        for_ = args['for_']
        return for_ is self.value


@dataclass
class ResourcePredicate(Predicate):
    value: Type[Resource]
    key: str = 'resource'

    def matches(self, request: Request, **args) -> bool:
        resource = args.get('resource', request.resource)
        resource_class = resource.__class__
        return resource_class is self.value


@dataclass
class ResourceIdPredicate(Predicate):
    """ Match on the resource id of yourself """

    value: str
    key: str = 'resourceid'
    rank: int = 30

    def matches(self, request: Request, **args) -> bool:
        resource = args.get('resource', request.resource)
        resourceid = resource.id
        return self.value == resourceid


@dataclass
class ParentIdPredicate(Predicate):
    """ Match on the resource id of a parent """

    value: str
    key: str = 'parentid'
    rank: int = 20

    def matches(self, request: Request, **args) -> bool:
        resource = args.get('resource', request.resource)
        return self.value in resource.parentids


@dataclass
class TemplateStringPredicate(Predicate):
    """ Non-matching predicate to provide rendering info """

    value: str
    key: str = 'template_string'

    def __str__(self):
        return f'{self.key}'

    def matches(self, request: Request, **args) -> bool:
        raise NotImplementedError


@dataclass
class RendererPredicate(Predicate):
    """ Non-matching predicate for the renderer adapter """

    value: Type[Any]
    key: str = 'renderer'

    def __str__(self):
        return f'{self.key}'

    def matches(self, request: Request, **args) -> bool:
        raise NotImplementedError

