from typing import Type, Mapping, Union

from kaybee_component.predicate_action import PredicateAction
from kaybee_component.predicates import ForPredicate, ResourcePredicate
from kaybee_component.services.request.base_request import Request


class RequestForPredicate(ForPredicate):
    value: Type[Request]


class RequestAction(PredicateAction):
    REQUIRED_PREDICATES = (RequestForPredicate,)
    OPTIONAL_PREDICATES = (ResourcePredicate,)
    predicates: Mapping[str, Union[ForPredicate, ResourcePredicate]]
