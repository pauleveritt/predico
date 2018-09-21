import pytest

from kaybee_component.service.manager import InvalidInjectable


def test_construction(sm):
    assert True is sm.config.debug
    assert 'TestServiceRegistry' == sm.registry.__name__
    assert {} == sm.services


def test_register_services(register_services, initialized_sm):
    assert 2 == len(initialized_sm.registry.config.services)
    services = initialized_sm.services
    assert ('request', 'view') == tuple(services.keys())


def test_valid_injected(register_services, initialized_sm):
    services = initialized_sm.services
    sm_config = initialized_sm.config

    # Test the view service
    viewservice = services['view']
    viewservice_config = sm_config.serviceconfigs['viewservice']
    assert viewservice_config.flag == viewservice.config.flag

    # Test the request service
    requestservice = services['request']
    requestservice_config = sm_config.serviceconfigs['requestservice']
    assert requestservice_config.flag == requestservice.config.flag

def test_valid_injectedattr(register_services, initialized_sm):
    services = initialized_sm.services
    sm_config = initialized_sm.config
    view = services['view']
    serviceconfigs = sm_config.serviceconfigs
    assert serviceconfigs == view.allconfigs


def test_invalid_injectable(invalid_injectable_type, sm):
    with pytest.raises(InvalidInjectable) as exc:
        sm.initialize()
