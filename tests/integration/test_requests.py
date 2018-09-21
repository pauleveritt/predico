from kaybee_component.services.request.service import RequestService


def test_request(test_registry, initialized_sm):
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
    view = request.view
    assert 911 == view
