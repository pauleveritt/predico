from dataclasses import dataclass

from predico import registry
from predico.injector import inject
from predico.registry import Registry
from predico.servicemanager.base_service import BaseService
from predico.servicemanager.manager import ServiceManager
from predico.services.view.action import ViewAction
from predico.services.view.base_view import IndexView
from predico.services.view.config import ViewServiceConfig


@registry.service(name='view')
@dataclass(frozen=True)
class ViewService(BaseService):
    sm: ServiceManager
    registry: Registry
    config: ViewServiceConfig

    def get_view(self, request, for_=IndexView):
        """ Use the predicate registry to find the right view class """

        # Grab ViewAction and use sorted_actions to find first match
        sorted_actions = ViewAction.sorted_actions(self.registry)

        # Find the first action which matches the args
        for action, view_class in sorted_actions:
            if action.all_predicates_match(request, for_=for_):

                # Use dependency injection to make an instance of
                # that view class
                view_instance = inject(
                    dict(),  # props
                    self.get_injectables(request),
                    view_class,
                    request=request
                )
                return view_instance

        # No matches, return None
        return None
