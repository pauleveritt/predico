from kaybee_component.services.request.service import RequestService
from tests.conftest import ForView1


def test_request(initialized_sm):
    test_registry = initialized_sm.registry
    services = initialized_sm.services
    request_service: RequestService = services['request']

    # The outside world (the system) initiates the making of a
    # request, passing in the data needed for that kind of request,
    # e.g. a SphinxRequest. Perhaps a callable is passed into
    # RequestServiceConfig, or an adapter is registered.
    request = request_service.make_request(
        sm=initialized_sm,
        resource_id='more/about',
        app_registry=test_registry,
    )
    view: ForView1 = request.view
    assert 'ForView1' in view.__class__.__name__
    assert 99 == view.viewservice_config.flag
