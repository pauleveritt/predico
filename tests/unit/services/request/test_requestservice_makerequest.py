def test_has_make_request(requestservice):
    assert hasattr(requestservice, 'make_request')


def test_make_request(requestservice):
    request = requestservice.make_request('more/about')
    assert 'more/about' == request.resourceid
    assert requestservice.sm == request.sm
    assert requestservice.registry == request.registry


def test_get_request_resource(requestservice, resourceservice, fake_article1):
    resourceservice.resources[fake_article1.id] = fake_article1
    request = requestservice.make_request('more/article1')
    assert 'more/article1' == request.resource.id


def test_get_request_view(fakearticle_view, requestservice, resourceservice,
                          fake_article1):
    resourceservice.resources[fake_article1.id] = fake_article1
    request = requestservice.make_request('more/article1')
    assert 'Fake Article View' == request.view.name
