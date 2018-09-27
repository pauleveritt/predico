from dataclasses import dataclass

from kaybee_component import registry
from kaybee_component.injector import inject
from kaybee_component.registry import Registry
from kaybee_component.service.base_service import BaseService
from kaybee_component.service.manager import ServiceManager
from kaybee_component.services.resource.base_resource import Resource
from kaybee_component.services.view.action import ViewAction
from kaybee_component.services.view.base_view import IndexView
from kaybee_component.services.view.config import ViewServiceConfig


@registry.service(name='view')
@dataclass(frozen=True)
class ViewService(BaseService):
    sm: ServiceManager
    app_registry: Registry
    config: ViewServiceConfig

    def get_view(self, request, for_=IndexView):
        """ Use the predicate registry to find the right view class """
        view_class = ViewAction.get_class(request, for_)

        # Use dependency injection to make an instance of that view class
        view_instance = inject(
            dict(),  # props
            self.sm.injectables,
            view_class
        )
        return view_instance
