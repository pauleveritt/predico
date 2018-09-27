from typing import Type, Mapping, Union

from kaybee_component.predicate_action import PredicateAction
from kaybee_component.predicates import (
    ForPredicate, ResourcePredicate,
    ResourceIdPredicate,
    ParentIdPredicate
)
from kaybee_component.services.view.base_view import IndexView


class ViewForPredicate(ForPredicate):
    value: Type[IndexView]


class ViewAction(PredicateAction):
    action_name = 'view'
    REQUIRED_PREDICATES = (ViewForPredicate,)
    OPTIONAL_PREDICATES = (
    ResourcePredicate, ResourceIdPredicate, ParentIdPredicate)
    predicates: Mapping[
        str, Union[
            ForPredicate, ResourcePredicate, ResourceIdPredicate, ParentIdPredicate]]
