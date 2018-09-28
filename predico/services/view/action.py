from typing import Type, Mapping, Union

from predico.predicate_action import PredicateAction
from predico.predicates import (
    ForPredicate, ResourcePredicate,
    ResourceIdPredicate,
    ParentIdPredicate
)
from predico.services.view.base_view import IndexView


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
