from typing import Mapping, Union

from kaybee_component.predicate_action import PredicateAction
from kaybee_component.predicates import ForPredicate, ResourcePredicate


class ResourceAction(PredicateAction):
    REQUIRED_PREDICATES = ()
    OPTIONAL_PREDICATES = ()
    predicates: Mapping[str, Union[ForPredicate, ResourcePredicate]]
