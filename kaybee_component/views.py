from typing import Type, Mapping, Union

from kaybee_component.predicate_action import PredicateAction
from kaybee_component.predicates import ForPredicate, ResourcePredicate
from kaybee_component.viewtypes import IndexView


class ViewForPredicate(ForPredicate):
    value: Type[IndexView]


class ViewAction(PredicateAction):
    REQUIRED_PREDICATES = (ForPredicate,)
    OPTIONAL_PREDICATES = (ResourcePredicate,)
    predicates: Mapping[str, Union[ForPredicate, ResourcePredicate]]
