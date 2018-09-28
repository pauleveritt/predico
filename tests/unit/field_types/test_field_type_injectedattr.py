from predico.field_types import injectedattr


class BogusResource:
    pass


def test_basic():
    i = injectedattr(BogusResource, 'title')
    assert BogusResource == i.metadata['injectedattr']['type_']
    assert 'title' == i.metadata['injectedattr']['attr']


def test_other_data():
    # Ensure the field can have other stuff in it
    i = injectedattr(BogusResource, 'title', metadata=dict(a=1), init=False)
    assert BogusResource == i.metadata['injectedattr']['type_']
    assert 'title' == i.metadata['injectedattr']['attr']
    assert 1 is i.metadata['a']
    assert False is i.init
