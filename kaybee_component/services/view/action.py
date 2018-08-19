from typing import Type, Mapping, Union

from kaybee_component.predicate_action import PredicateAction
from kaybee_component.predicates import ForPredicate, ResourcePredicate
from kaybee_component.services.view.base_view import IndexView


class ViewForPredicate(ForPredicate):
    value: Type[IndexView]


class ViewAction(PredicateAction):
    REQUIRED_PREDICATES = (ViewForPredicate,)
    OPTIONAL_PREDICATES = (ResourcePredicate,)
    predicates: Mapping[str, Union[ForPredicate, ResourcePredicate]]
