from typing import Type, Mapping, Union

from predico.predicate_action import PredicateAction
from predico.predicates import ForPredicate, ResourcePredicate
from predico.services.request.base_request import Request


class RequestForPredicate(ForPredicate):
    value: Type[Request]


class RequestAction(PredicateAction):
    REQUIRED_PREDICATES = (RequestForPredicate,)
    OPTIONAL_PREDICATES = (ResourcePredicate,)
    predicates: Mapping[str, Union[ForPredicate, ResourcePredicate]]
