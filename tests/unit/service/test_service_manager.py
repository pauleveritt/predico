import pytest

from kaybee_component.service.manager import ServiceManager, InvalidInjectable


class TestServiceManager:
    def test_import(self):
        assert 'ServiceManager' == ServiceManager.__name__

    def test_construction(self, sm):
        assert True is sm.config.debug
        assert 'TestServiceRegistry' == sm.registry.__name__
        assert {} == sm.services

    def test_register_services(self, register_services, initialized_sm):
        assert 2 == len(initialized_sm.registry.config.services)
        services = initialized_sm.services
        assert ('view', 'request') == tuple(services.keys())
        view = services['view']
        assert initialized_sm.config.debug == view.sm_config.debug

    def test_invalid_injectable(self, invalid_injectable_type, sm):
        with pytest.raises(InvalidInjectable) as exc:
            sm.initialize()
