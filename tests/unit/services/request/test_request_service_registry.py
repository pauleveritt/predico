import dectate

from kaybee_component.service.configuration import ServiceManagerConfig
from kaybee_component.service.manager import ServiceManager
from kaybee_component.service.registry import ServiceRegistry
from kaybee_component.services.request import register
from kaybee_component.services.request.config import RequestServiceConfig
from kaybee_component.services.request.registry import BaseRequestRegistry
from kaybee_component.services.request.service import RequestService


def test_import():
    assert 'BaseRequestRegistry' == BaseRequestRegistry.__name__


def test_construction(rs_registry):
    dectate.commit(rs_registry)
    requests = rs_registry.config.requests
    assert 0 == len(requests)


def test_whole_damn_thing():
    rs_config = RequestServiceConfig(flag=99)

    sm_config = ServiceManagerConfig(
        serviceconfigs=dict(
            requestservice=rs_config,
        )
    )

    class sm_registry(ServiceRegistry):
        pass

    sm = ServiceManager(sm_config, sm_registry)

    register(sm)
    dectate.commit(sm.registry)

    query = dectate.Query('service')
    services = list(query(sm.registry))
    request_service: RequestService = services[0][1]
    assert 'RequestService' == request_service.__name__

    service = request_service(registry=BaseRequestRegistry, config=rs_config)
