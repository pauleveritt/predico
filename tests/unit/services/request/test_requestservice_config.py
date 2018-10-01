from predico.services.request.common_request import CommonRequest


def test_construction(requestservice_config):
    assert CommonRequest == requestservice_config.factory
