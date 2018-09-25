from kaybee_component.services.request.service import RequestService


# Make a custom view for 'more/contact' and register it

def test_default_view(initialized_sm, test_resources):
    """ Get the default IndexView """
    # Get the request service
    services = initialized_sm.services
    request_service: RequestService = services['request']

    # The outside world (the system) initiates the making of a
    # request, passing in the data needed for that kind of request,
    # e.g. a SphinxRequest. Perhaps a callable is passed into
    # RequestServiceConfig, or an adapter is registered.
    request = request_service.make_request(resourceid='more/index')

    # Request: Did the request get the correct one?
    assert 'more/index' == request.resource.id

    # View: Did the request get the correct one?
    view = request.view
    assert 'TestResourceView' in view.__class__.__name__
    assert 99 == view.viewservice_config.flag
    assert 'Generic Resource View' == view.name


def test_resourceclass_view(initialized_sm, test_resources):
    """ Get a view registered for a resource type """
    # Get the request service
    services = initialized_sm.services
    request_service: RequestService = services['request']

    request = request_service.make_request(resourceid='more/contact')

    # Request: Did the request get the correct one?
    assert 'more/contact' == request.resource.id

    # View: Did the request get the correct one?
    view = request.view
    assert 'TestSectionView' in view.__class__.__name__
    assert 99 == view.viewservice_config.flag
    assert 'Section View' == view.name


def test_self_view(initialized_sm, test_resources):
    """ Get a view registered for a specific resource """
    # Get the request service
    services = initialized_sm.services
    request_service: RequestService = services['request']

    request = request_service.make_request(resourceid='more/specificid')

    # Request: Did the request get the correct one?
    assert 'more/specificid' == request.resource.id

    # View: Did the request get the correct one?
    view = request.view
    assert 'TestSectionView' in view.__class__.__name__
    assert 99 == view.viewservice_config.flag
    assert 'Section View' == view.name
