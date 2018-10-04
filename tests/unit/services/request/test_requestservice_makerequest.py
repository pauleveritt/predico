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
    assert hasattr(request, 'resource')
    assert hasattr(request, 'view')
    assert hasattr(request, 'adapters')


def test_get_request_view(fakearticle_view, requestservice, resourceservice,
                          fake_article1):
    resourceservice.resources[fake_article1.id] = fake_article1
    request = requestservice.make_request('more/article1')
    assert 'Fake Article View' == request.view.name


def test_get_request_adapters(fakearticle_adapter, requestservice,
                              resourceservice,
                              fake_article1, fake_breadcrumbs_resources):
    resourceservice.resources[fake_article1.id] = fake_article1
    request = requestservice.make_request('more/article1')

    adapter = request.adapters[fake_breadcrumbs_resources]
    assert 'Fake Breadcrumbs Resources' == adapter.name


def test_adapt_resource(fakearticle_adapter, requestservice,
                        resourceservice, fake_article1, fake_article2,
                        fake_breadcrumbs_resources):
    resourceservice.resources[fake_article1.id] = fake_article1
    request = requestservice.make_request('more/article1')

    adapter = request.adapt_resource(fake_breadcrumbs_resources, fake_article2)
    assert 'Fake Breadcrumbs Resources' == adapter.name
    assert 'more/article2' == adapter.resource.id
