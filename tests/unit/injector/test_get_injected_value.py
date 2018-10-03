import pytest

from predico.injector import get_injected_value


class NonCallableSource(dict):
    name = 'Non-Callable Source'


class CallableSource:
    flag: int = 27

    def __call__(self):
        return 'Callable Source'


def test_get_injected_value_attr():
    """ Handle the ``injected`` field type's attr operation """

    field_metadata = dict(attr='name')
    source = NonCallableSource()
    value = get_injected_value(field_metadata, source)
    assert 'Non-Callable Source' == value


def test_get_injected_value_missing_attr():
    """ Handle the ``injected`` field type's attr operation w/ no value """

    field_metadata = dict(attr='nobody_home')
    source = NonCallableSource()
    value = get_injected_value(field_metadata, source)
    assert None is value


def test_get_injected_value_key():
    """ Handle the ``injected`` field type's key operation """

    field_metadata = dict(key='first')
    source = NonCallableSource()
    source['first'] = 'First'
    value = get_injected_value(field_metadata, source)
    assert 'First' == value


def test_get_injected_value_missing_key():
    """ Handle the ``injected`` field type's key missing operation """

    field_metadata = dict(key='first')
    source = NonCallableSource()
    source['second'] = 'First'
    with pytest.raises(KeyError):
        get_injected_value(field_metadata, source)


def test_get_injected_value_callable():
    """ Handle the ``injected`` field type's call operation """

    field_metadata = dict(call=True)
    source = CallableSource()
    value = get_injected_value(field_metadata, source)
    assert 'Callable Source' == value


def test_get_injected_value_no_call():
    """ Instruct a callable to not call via call=False """

    field_metadata = dict(call=False)
    source = CallableSource()
    value = get_injected_value(field_metadata, source)
    assert 27 == value.flag


def test_get_injected_value_noncallable():
    """ Handle the ``injected`` field type's non-callable operation """

    field_metadata = dict(call=False)
    source = NonCallableSource()
    injectable = get_injected_value(field_metadata, source)
    assert 'Non-Callable Source' == injectable.name
