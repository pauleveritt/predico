from kaybee_component.services.request.service import RequestService


def test_pydantic_resourceid_view(initialized_sm, test_resources):
    """ Get a view registered for a specific resource """
    # Get the request service
    services = initialized_sm.services
    request_service: RequestService = services['request']

    request = request_service.make_request(resourceid='pydantic/about')

    # Request: Did the request get the correct one?
    assert 'pydantic/about' == request.resource.id

    # View: Did the request get the correct one?
    view = request.view
    assert 'TestPydanticView' in view.__class__.__name__
    assert 99 == view.viewservice_config.flag
    assert 'One Pydantic View' == view.name
