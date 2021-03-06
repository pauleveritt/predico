import pytest

from predico.services.request.common_request import CommonRequest


def test_unintialized(uninitialized_sm):
    assert True is uninitialized_sm.config.debug
    assert 'TestServiceRegistry' == uninitialized_sm.registry.__name__
    assert {} == uninitialized_sm.services


def test_register_services(initialized_sm):
    services = initialized_sm.services
    assert ['adapter', 'request', 'resource', 'view'] == sorted(
        tuple(services.keys()))


def test_valid_injected(initialized_sm):
    services = initialized_sm.services
    sm_config = initialized_sm.config

    # Test the view service
    viewservice = services['view']
    viewservice_config = sm_config.serviceconfigs['viewservice']
    assert viewservice_config.flag == viewservice.config.flag

    # Test the request service
    requestservice = services['request']
    requestservice_config = sm_config.serviceconfigs['requestservice']
    assert CommonRequest == requestservice.config.factory


def test_valid_injectedattr(initialized_sm):
    services = initialized_sm.services
    sm_config = initialized_sm.config
    view = services['view']
    viewservice_config = sm_config.serviceconfigs['viewservice']
    assert viewservice_config == view.config


def test_add_good_injectable(initialized_sm):
    class ValidInjectable:
        pass

    vi = ValidInjectable()
    assert ValidInjectable.__name__ not in initialized_sm.injectables
    initialized_sm.add_injectable(vi)
    assert ValidInjectable.__name__ in initialized_sm.injectables


def test_invalid_injectable(invalid_injectable_type, uninitialized_sm):
    with pytest.raises(TypeError) as exc:
        uninitialized_sm.initialize()
