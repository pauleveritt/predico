from kaybee_component.predicates import ForPredicate
from kaybee_component.views import View


class TestForPredicate:
    def test_import(self):
        assert 'ForPredicate' == ForPredicate.__name__

    def test_construction(self):
        predicate = ForPredicate(value=View)
        assert 'for_' == predicate.key

