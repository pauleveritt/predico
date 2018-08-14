import dectate
import pytest

from kaybee_component.predicate_registry import PluginApp


@pytest.fixture
def registry():
    class TestApp(PluginApp):
        pass

    return TestApp


@pytest.fixture
def register_plugins(registry):
    @PluginApp.plugin('a')
    def f():
        pass  # do something interesting

    @PluginApp.plugin('b')
    def g():
        pass  # do something interesting

    dectate.commit(registry)

def test_plugins(registry, register_plugins):
    plugins = sorted(registry.config.plugins.items())
    assert 'a' == plugins[0][0]
