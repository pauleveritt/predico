from predico.services.request.service import RequestService


def test_default_breadcrumbs_adapter(initialized_sm, test_resources,
                                     fake_breadcrumbs_resources):
    """ Get the default BreadcrumbResources adapter """

    # Get the request service
    services = initialized_sm.services
    request_service: RequestService = services['request']

    # Make a request for a Section
    request = request_service.make_request(resourceid='about/index')

    # Request: Did the request get the correct one?
    assert 'about/index' == request.resource.id

    # Adapter: Did the request get the correct one?
    adapter = request.adapters[fake_breadcrumbs_resources]
    assert 'FakeBreadcrumbsResources' in adapter.__class__.__name__
    assert 'Fake Breadcrumbs Resources' == adapter.name
    assert 'About Section' == adapter.resource_title


def test_resourceclass_adapter(initialized_sm, test_resources,
                               fake_breadcrumbs_resources):
    """ Get an adapter registered for a resource type """

    # Get the request service
    services = initialized_sm.services
    request_service: RequestService = services['request']

    # Make a request for an Article
    request = request_service.make_request(resourceid='news/first')

    # Request: Did the request get the correct one?
    assert 'news/first' == request.resource.id

    # Adapter: Did the request get the correct one?
    adapter = request.adapters[fake_breadcrumbs_resources]
    assert 'FakeArticleBreadcrumbsResources' in adapter.__class__.__name__
    assert 'Fake Article Breadcrumbs Resources' == adapter.name
    assert 'Contact' == adapter.resource_title


def test_resourceid_adapter(initialized_sm, test_resources,
                            fake_breadcrumbs_resources):
    """ Get an adapter registered for a resourceid """

    # Get the request service
    services = initialized_sm.services
    request_service: RequestService = services['request']

    # Make a request for an Article
    request = request_service.make_request(
        resourceid='injected/resourceidadapter')

    # Request: Did the request get the correct one?
    assert 'injected/resourceidadapter' == request.resource.id

    # Adapter: Did the request get the correct one?
    adapter = request.adapters[fake_breadcrumbs_resources]
    assert 'FakeResourceIdBreadcrumbsResources' in adapter.__class__.__name__
    assert 'Fake ResourceId Breadcrumbs Resources' == adapter.name
    assert 'Injected ResourceId Adapter Article' == adapter.resource_title


def test_parentid_adapter(initialized_sm, test_resources,
                          fake_breadcrumbs_resources):
    """ Get an adapter registered for a parentid """

    # Get the request service
    services = initialized_sm.services
    request_service: RequestService = services['request']

    # Make a request for an Article
    request = request_service.make_request(resourceid='pydantic/about')

    # Request: Did the request get the correct one?
    assert 'pydantic/about' == request.resource.id

    # Adapter: Did the request get the correct one?
    adapter = request.adapters[fake_breadcrumbs_resources]
    assert 'FakeParentIdBreadcrumbsResources' in adapter.__class__.__name__
    assert 'Fake ParentId Breadcrumbs Resources' == adapter.name
    assert 'Pydantic Section' == adapter.resource_title


def test_defaultadapter_view(initialized_sm, test_resources,
                             fake_breadcrumbs_resources):
    """ Get a view with a default adapter injected """

    # This is the holy grail: a view or component or whatever which
    # can express as a dependency an adapter. The system then:
    # - Finds the most appropriate adapter
    # - Constructs that adapter using DI
    # - Then, injects that adapter instance into the view/component

    # Get the request service
    services = initialized_sm.services
    request_service: RequestService = services['request']

    request = request_service.make_request(
        resourceid='injected/defaultadapter')

    # Request: Did the request get the correct one?
    assert 'injected/defaultadapter' == request.resource.id

    # View: Did the request get the correct one?
    view = request.view
    assert 'TestInjectedDefaultAdapterView' in view.__class__.__name__
    assert 99 == view.viewservice_config.flag
    assert 'Use a Default Injected Adapter' == view.name

    # Now the fun part...did we get the adapter
    assert 'Injected Default Adapter Article' == \
           view.breadcrumbs_resources.resource_title


def test_specificadapter_view(initialized_sm, test_resources,
                              fake_breadcrumbs_resources):
    """ Get a view with a specific adapter injected """

    # Get the request service
    services = initialized_sm.services
    request_service: RequestService = services['request']

    request = request_service.make_request(
        resourceid='injected/resourceidadapter')

    # Request: Did the request get the correct one?
    assert 'injected/resourceidadapter' == request.resource.id

    # View: Did the request get the correct one?
    view = request.view
    assert 'TestInjectedResourceIdAdapterView' in view.__class__.__name__
    assert 99 == view.viewservice_config.flag
    assert 'Use a ResourceId Injected Adapter' == view.name

    # Now the fun part...did we get the adapter
    bcr = view.breadcrumbs_resources
    assert 'Injected ResourceId Adapter Article' == bcr.resource_title

    # Adapter: Did the request get the correct one?
    adapter = request.adapters[fake_breadcrumbs_resources]
    assert 'FakeResourceIdBreadcrumbsResources' in adapter.__class__.__name__
    assert 'Fake ResourceId Breadcrumbs Resources' == adapter.name
    assert 'Injected ResourceId Adapter Article' == adapter.resource_title


def test_injectedattr_adapter_view(initialized_sm, test_resources,
                                   fake_breadcrumbs_resources):
    """ View uses the attribute of an adapter """

    # Get the request service
    services = initialized_sm.services
    request_service: RequestService = services['request']

    request = request_service.make_request(
        resourceid='pydantic/injectedattr')

    # Request: Did the request get the correct one?
    assert 'pydantic/injectedattr' == request.resource.id

    # View: Did the request get the correct one?
    view = request.view
    assert 'TestInjectedattrResourceIdAdapterView' == view.__class__.__name__
    assert 99 == view.viewservice_config.flag
    assert 'Use a ResourceId Injectedattr Adapter' == view.name

    # Now the fun part...did we get the adapter
    bcr = view.breadcrumbs_resources
    assert 'Pydantic Injectedattr Section' == bcr.resource_title
