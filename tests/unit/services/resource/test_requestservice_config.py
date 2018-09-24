from kaybee_component.services.request.config import RequestServiceConfig


def test_construction():
    requestservice_config = RequestServiceConfig(flag=99)
    assert 99 == requestservice_config.flag
