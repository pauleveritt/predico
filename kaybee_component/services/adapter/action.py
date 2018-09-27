from typing import Type, Mapping, Union

from kaybee_component.predicate_action import PredicateAction
from kaybee_component.predicates import (
    ForPredicate, ResourcePredicate,
    ResourceIdPredicate,
    ParentIdPredicate
)
from kaybee_component.services.adapter.base_adapter import BaseAdapter


class AdapterForPredicate(ForPredicate):
    value: Type[BaseAdapter]


class AdapterAction(PredicateAction):
    action_name = 'adapter'
    REQUIRED_PREDICATES = (AdapterForPredicate,)
    OPTIONAL_PREDICATES = (
        ResourcePredicate, ResourceIdPredicate, ParentIdPredicate)
    predicates: Mapping[
        str, Union[
            ForPredicate, ResourcePredicate, ResourceIdPredicate,
            ParentIdPredicate]]
