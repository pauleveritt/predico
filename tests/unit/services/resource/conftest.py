import pytest

from kaybee_component.services.resource.service import ResourceService


class ServiceManager:
    flag = 1

    def foo(self):
        return 'bar'


class Registry:
    flag = 2


class ResourceServiceConfig:
    flag = 3


@pytest.fixture
def sm(mocker):
    return mocker.patch('conftest.ServiceManager')


@pytest.fixture
def app_registry(mocker):
    return mocker.patch('conftest.Registry')


@pytest.fixture
def config(mocker):
    return mocker.patch('conftest.ResourceServiceConfig')


@pytest.fixture
def resourceservice(sm, app_registry, config):
    sm.flag = 1234
    sm.foo.return_value = 8765
    return ResourceService(
        sm=sm,
        app_registry=app_registry,
        config=config
    )
