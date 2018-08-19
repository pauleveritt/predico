from kaybee_component.services.request.config import RequestServiceConfig


def test_import():
    assert 'RequestServiceConfig' == RequestServiceConfig.__name__


def test_construction(requestservice_config):
    assert 99 == requestservice_config.flag
