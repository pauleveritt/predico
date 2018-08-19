from kaybee_component.service.manager import ServiceManager


class TestServiceManager:
    def test_import(self):
        assert 'ServiceManager' == ServiceManager.__name__

    def test_construction(self, sm):
        assert True is sm.config.debug
        assert 'TestServiceRegistry' == sm.registry.__name__
