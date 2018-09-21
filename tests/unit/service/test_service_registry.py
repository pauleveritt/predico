import dectate

from kaybee_component.service.registry import services


def test_import():
    assert 'services' == services.__name__


def test_construction(sm_registry):
    dectate.commit(sm_registry)
    s = sm_registry.config.services
    assert 0 == len(s)
