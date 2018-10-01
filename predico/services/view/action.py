from typing import Mapping, Union

from predico.predicate_action import PredicateAction
from predico.predicates import (
    ResourcePredicate,
    ResourceIdPredicate,
    ParentIdPredicate,
    TemplateStringPredicate,
    RendererPredicate
)


class ViewAction(PredicateAction):
    action_name = 'view'
    REQUIRED_PREDICATES = ()
    OPTIONAL_PREDICATES = (
        ResourcePredicate, ResourceIdPredicate, ParentIdPredicate)
    NONLOOKUP_PREDICATES = (
        TemplateStringPredicate, RendererPredicate
    )
    predicates: Mapping[
        str, Union[
            ResourcePredicate, ResourceIdPredicate, ParentIdPredicate,
            TemplateStringPredicate, RendererPredicate
        ]]
