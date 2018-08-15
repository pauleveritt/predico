import inspect

import dectate
import pytest

from kaybee_component.predicate_registry import Kaybee


@pytest.fixture
def registry():
    class TestApp(Kaybee):
        pass

    return TestApp


@pytest.fixture
def register_plugins(registry):
    @registry.service('component')
    def f():
        pass  # do something interesting

    @Kaybee.service('render')
    def g():
        pass  # do something interesting

    @Kaybee.adapter('sidebar')
    def h():
        pass  # do something interesting

    dectate.commit(Kaybee)
    dectate.commit(registry)


def test_plugins(registry, register_plugins):
    c = Kaybee.config
    plugins = sorted(registry.config.plugins.items())
    kaybee_plugins = sorted(Kaybee.config.plugins.items())
    assert 3 == len(plugins)
    assert 2 == len(kaybee_plugins)
    assert 'component' == plugins[0][0]

    class Hello:
        pass

    def foo(bar: int, baz: str) -> int:
        return 9

    p = [
        (i[0], i[1].annotation)
        for i in inspect.signature(foo).parameters.items()
    ]

    assert 9 == p
