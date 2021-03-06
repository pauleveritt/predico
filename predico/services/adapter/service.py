from dataclasses import dataclass
from typing import Type, Any, Optional

from predico import registry
from predico.injector import inject
from predico.registry import Registry
from predico.servicemanager.base_service import BaseService
from predico.servicemanager.manager import ServiceManager
from predico.services.adapter.action import AdapterAction
from predico.services.adapter.base_adapter import Adapter
from predico.services.adapter.config import AdapterServiceConfig


@registry.service(name='adapter')
@dataclass(frozen=True)
class AdapterService(BaseService):
    sm: ServiceManager
    registry: Registry
    config: AdapterServiceConfig

    def get_adapter(self,
                    request,
                    for_: Type[Any],
                    **kwargs
                    ) -> Optional[Adapter]:
        """ Use the predicate registry to find the right adapter class """

        # Grab AdapterAction and use sorted_actions to find first match
        sorted_actions = AdapterAction.sorted_actions(self.registry)

        # Find the first action which matches the args
        for action, adapter_class in sorted_actions:
            if action.all_predicates_match(request, for_=for_, **kwargs):
                # Use dependency injection to make an instance of
                # that adapter class
                adapter_instance = inject(
                    kwargs,  # props
                    self.get_injectables(request),
                    adapter_class,
                    request=request
                )
                return adapter_instance

        # No matches, return None
        return None
