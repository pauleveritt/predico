import pytest

from kaybee_component.service.manager import InvalidInjectable


class TestServiceManager:
    def test_construction(self, sm):
        assert True is sm.config.debug
        assert 'TestServiceRegistry' == sm.registry.__name__
        assert {} == sm.services

    def test_register_services(self, register_services, initialized_sm):
        assert 2 == len(initialized_sm.registry.config.services)
        services = initialized_sm.services
        assert ('view', 'request') == tuple(services.keys())

    def test_valid_injected(self, register_services, initialized_sm):
        services = initialized_sm.services
        sm_config = initialized_sm.config
        view = services['view']
        viewservice_config = sm_config.serviceconfigs['viewservice']
        assert viewservice_config.flag == view.config.flag
        request = services['request']
        assert sm_config.debug == request.sm_config.debug

    def test_valid_injectedattr(self, register_services, initialized_sm):
        services = initialized_sm.services
        sm_config = initialized_sm.config
        view = services['view']
        serviceconfigs = sm_config.serviceconfigs
        assert serviceconfigs == view.allconfigs

    def test_invalid_injectable(self, invalid_injectable_type, sm):
        with pytest.raises(InvalidInjectable) as exc:
            sm.initialize()
