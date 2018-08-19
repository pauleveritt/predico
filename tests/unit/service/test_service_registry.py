import dectate

from kaybee_component.service.registry import ServiceRegistry


def test_import():
    assert 'ServiceRegistry' == ServiceRegistry.__name__


def test_construction(sm_registry):
    dectate.commit(sm_registry)
    services = sm_registry.config.services
    assert 0 == len(services)
