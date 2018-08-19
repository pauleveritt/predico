from kaybee_component.field_types import injected

def test_import():
    assert 'injected' == injected.__name__


def test_basic():
    i = injected()
    assert True is i.metadata['injected']


def test_other_data():
    i = injected(metadata=dict(a=1), init=False)
    assert True is i.metadata['injected']
    assert 1 is i.metadata['a']
    assert False is i.init
