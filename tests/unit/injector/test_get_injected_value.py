from predico.injector import get_injected_value


class NonCallableSource:
    name = 'Non-Callable Source'

    def __getitem__(self, key):
        return self.name


class CallableSource:
    def __call__(self):
        return 'Callable Source'


def test_get_injected_value_attr():
    """ Handle the ``injected`` field type's attr operation """

    field_metadata = dict(attr='name')
    source = NonCallableSource()
    value = get_injected_value(field_metadata, source)
    assert 'Non-Callable Source' == value


def test_get_injected_value_key():
    """ Handle the ``injected`` field type's key operation """

    field_metadata = dict(key='name')
    source = NonCallableSource()
    value = get_injected_value(field_metadata, source)
    assert 'Non-Callable Source' == value


def test_get_injected_value_callable():
    """ Handle the ``injected`` field type's call operation """

    field_metadata = dict(call=True)
    source = CallableSource()
    value = get_injected_value(field_metadata, source)
    assert 'Callable Source' == value


def test_get_injected_value_noncallable():
    """ Handle the ``injected`` field type's non-callable operation """

    field_metadata = dict(call=False)
    source = NonCallableSource()
    injectable = get_injected_value(field_metadata, source)
    assert 'Non-Callable Source' == injectable.name
