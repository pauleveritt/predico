from kaybee_component.service.configuration import ServiceManagerConfig


def test_import():
    assert 'ServiceManagerConfig' == ServiceManagerConfig.__name__


def test_construction(sm_config):
    assert True is sm_config.debug
