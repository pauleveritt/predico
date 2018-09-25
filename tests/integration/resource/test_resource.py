def test_resources_empty(rs):
    assert {} == rs.resources


def test_add_get_resource(rs):
    resourceid = 'more/contact'
    resource = rs.add_resource(rtype='testarticle', id=resourceid,
                               title='More')
    assert resourceid == resource.id
    assert resource == rs.resources[resourceid]


def test_request_resource(services, test_resources):
    request_service = services['request']

    # The outside world (the system) initiates the making of a
    # request, passing in the data needed for that kind of request,
    # e.g. a SphinxRequest. Perhaps a callable is passed into
    # RequestServiceConfig, or an adapter is registered.
    request = request_service.make_request(resourceid='more/contact')

    # Request: Did the request get the correct one?
    assert 'more/contact' == request.resource.id
