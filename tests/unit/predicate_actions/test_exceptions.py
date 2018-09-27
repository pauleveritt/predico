"""

Test some of the custom exceptions.

"""
import pytest

from kaybee_component.predicate_action import (
    UnknownArgument,
    MissingArgument,
    LookupMissingRequired,
    UnknownLookup
)


def test_unknown_argument():
    with pytest.raises(UnknownArgument) as exc:
        m = UnknownArgument.fmt.format(name='xxx')
        raise UnknownArgument(m)
    assert 'Decorator supplied unknown predicate: xxx' == str(exc.value)


def test_missing_argument():
    with pytest.raises(MissingArgument) as exc:
        m = MissingArgument.fmt.format(name='xxx')
        raise MissingArgument(m)
    assert '__init__() missing 1 required positional argument: xxx' == str(
        exc.value)


def test_lookup_missing_argument():
    with pytest.raises(LookupMissingRequired) as exc:
        m = LookupMissingRequired.fmt.format(name='xxx')
        raise LookupMissingRequired(m)
    assert 'Lookup is missing required field: xxx' == str(exc.value)


def test_predicate_matches_lookup():
    with pytest.raises(UnknownLookup) as exc:
        m = UnknownLookup.fmt.format(name='xxx')
        raise UnknownLookup(m)
    assert 'Lookup supplied unknown predicate argument: xxx' == str(exc.value)
