def test_has_get_adapter(adapterservice):
    assert hasattr(adapterservice, 'get_adapter')


def test_get_adapter_for(
        fakefor_adapter,
        adapterservice, fake_resource1,
        fake_breadcrumbs_resources,
        fake_request_class
):
    # Registrations:
    # a. for_=FakeBreadcrumbsResources
    # Request:
    # - resource is FakeResource
    # Expected:
    # - (a)
    fake_request = fake_request_class(resource=fake_resource1)
    adapter = adapterservice.get_adapter(fake_request,
                                         for_=fake_breadcrumbs_resources)
    assert 'Fake Breadcrumbs Resources' == adapter.name


#  ---- resource: non-matching and matching

def test_get_adapter_for_nomatch_resource(
        fakefor_adapter, fakearticle_adapter,
        adapterservice, fake_resource1,
        fake_breadcrumbs_resources,
        fake_request_class
):
    # Registrations:
    # a. for_=FakeBreadcrumbsResources
    # b. for_=FakeBreadcrumbsResources, resource=FakeArticle
    # Request:
    # - resource is FakeResource
    # Expected:
    # - (a)
    fake_request = fake_request_class(resource=fake_resource1)
    adapter = adapterservice.get_adapter(fake_request,
                                         for_=fake_breadcrumbs_resources)
    assert 'Fake Breadcrumbs Resources' == adapter.name


def test_get_adapter_for_match_resource(
        fakefor_adapter, fakearticle_adapter,
        adapterservice, fake_article1,
        fake_breadcrumbs_resources,
        fake_request_class
):
    # Registrations:
    # a. for_=FakeBreadcrumbsResources
    # b. for_=FakeBreadcrumbsResources, resource=FakeArticle
    # Request:
    # - resource is FakeArticle
    # Expected:
    # - (b)
    fake_request = fake_request_class(resource=fake_article1)
    adapter = adapterservice.get_adapter(fake_request,
                                         for_=fake_breadcrumbs_resources
                                         )
    assert 'Fake Article Adapter' == adapter.name


#  ---- resourceid: non-matching and matching

def test_get_adapter_for_nomatch_resourceid(
        fakefor_adapter, fakeresourceid_adapter,
        adapterservice, fake_article1,
        fake_breadcrumbs_resources,
        fake_request_class
):
    # Registrations:
    # a. for_=FakeBreadcrumbsResources
    # b. for_=FakeBreadcrumbsResources, resourceid='more/article2'
    # Request:
    # - resource is 'more/article1'
    # Expected:
    # - (a)
    fake_request = fake_request_class(resource=fake_article1)
    adapter = adapterservice.get_adapter(fake_request,
                                         for_=fake_breadcrumbs_resources
                                         )
    assert 'Fake Breadcrumbs Resources' == adapter.name


def test_get_adapter_for_match_resourceid(
        fakefor_adapter, fakeresourceid_adapter,
        adapterservice, fake_article2,
        fake_breadcrumbs_resources,
        fake_request_class
):
    # Registrations:
    # a. for_=FakeBreadcrumbsResources
    # b. for_=FakeBreadcrumbsResources, resourceid='more/article2'
    # Request:
    # - resource is 'more/article2'
    # Expected:
    # - (a)
    fake_request = fake_request_class(resource=fake_article2)
    adapter = adapterservice.get_adapter(fake_request,
                                         for_=fake_breadcrumbs_resources
                                         )
    assert 'Fake ResourceId Adapter' == adapter.name


#  ---- parentid: non-matching and matching

def test_get_adapter_for_nomatch_parentid(
        fakefor_adapter, fakeparentid_adapter,
        adapterservice, fake_blog1,
        fake_breadcrumbs_resources,
        fake_request_class
):
    # Registrations:
    # a. for_=FakeBreadcrumbsResources
    # b. for_=FakeBreadcrumbsResources, parentid='more/index'
    # Request:
    # - resource is 'blog/blog1'
    # Expected:
    # - (a)
    fake_request = fake_request_class(resource=fake_blog1)
    adapter = adapterservice.get_adapter(fake_request,
                                         for_=fake_breadcrumbs_resources
                                         )
    assert 'Fake Breadcrumbs Resources' == adapter.name


def test_get_adapter_for_match_parentid(
        fakefor_adapter, fakeparentid_adapter,
        adapterservice, fake_article2,
        fake_breadcrumbs_resources,
        fake_request_class
):
    # Registrations:
    # a. for_=FakeBreadcrumbsResources
    # b. for_=FakeBreadcrumbsResources, parentid='more/index'
    # Request:
    # - resource is 'more/article2'
    # Expected:
    # - (b)
    fake_request = fake_request_class(resource=fake_article2)
    adapter = adapterservice.get_adapter(fake_request,
                                         for_=fake_breadcrumbs_resources
                                         )
    assert 'Fake ParentId Adapter' == adapter.name


# ---- Combination: for_, resourceid, parentid

def test_get_adapter_for_parentid_match_resourceid(
        fakefor_adapter, fakeresourceid_adapter, fakeparentid_adapter,
        adapterservice, fake_article2,
        fake_breadcrumbs_resources,
        fake_request_class
):
    # Registrations:
    # a. for_=FakeBreadcrumbsResources
    # b. for_=FakeBreadcrumbsResources, parentid='more/index'
    # b. for_=FakeBreadcrumbsResources, resourceid='more/article2'
    # Request:
    # - resource is 'more/article2'
    # Expected:
    # - (c)
    fake_request = fake_request_class(resource=fake_article2)
    adapter = adapterservice.get_adapter(fake_request,
                                         for_=fake_breadcrumbs_resources
                                         )
    assert 'Fake ResourceId Adapter' == adapter.name


# ---- Combination: for_, resource, parentid

def test_get_adapter_for_resource_match_parentid(
        fakefor_adapter, fakeresource_adapter, fakeparentid_adapter,
        adapterservice, fake_article2,
        fake_breadcrumbs_resources,
        fake_request_class
):
    # Registrations:
    # a. for_=FakeBreadcrumbsResources
    # b. for_=FakeBreadcrumbsResources, parentid='more/index'
    # b. for_=FakeBreadcrumbsResources, resource=FakeArticle
    # Request:
    # - resource is 'more/article2'
    # Expected:
    # - (b)
    fake_request = fake_request_class(resource=fake_article2)
    adapter = adapterservice.get_adapter(fake_request,
                                         for_=fake_breadcrumbs_resources
                                         )
    assert 'Fake ParentId Adapter' == adapter.name


# ---- Combination: all 4

def test_get_adapter_for_resource_parentid_match_resourceid(
        fakefor_adapter, fakeresource_adapter, fakeparentid_adapter,
        fakeresourceid_adapter,
        adapterservice, fake_article2,
        fake_breadcrumbs_resources,
        fake_request_class
):
    # Registrations:
    # a. for_=FakeBreadcrumbsResources
    # b. for_=FakeBreadcrumbsResources, parentid='more/index'
    # c. for_=FakeBreadcrumbsResources, resourceid='more/article2'
    # d. for_=FakeBreadcrumbsResources, resource=FakeArticle
    # Request:
    # - resource is 'more/article2'
    # Expected:
    # - (c)
    fake_request = fake_request_class(resource=fake_article2)
    adapter = adapterservice.get_adapter(fake_request,
                                         for_=fake_breadcrumbs_resources)
    assert 'Fake ResourceId Adapter' == adapter.name


#  ---- args: Use resource passed-in rather than request.resource

def test_get_adapter_for_passed_in_resource(
        fakefor_adapter, fakesubresource_adapter,
        adapterservice, fake_article1, fake_article3,
        fake_reference_entry,
        fake_request_class
):
    # Registrations:
    # a. for_=FakeBreadcrumbsResources
    # b. for_=FakeBreadcrumbsResources, resourceid='more/article2'
    # Request:
    # - resource is 'more/article2'
    # - passed-in- resource is 'more/article1'
    # Expected:
    # - (a)
    fake_request = fake_request_class(resource=fake_article1)
    adapter = adapterservice.get_adapter(fake_request,
                                         for_=fake_reference_entry,
                                         resource=fake_article3,
                                         )
    assert 'Fake Subresource Adapter' == adapter.name
    assert 'subrequest' == adapter.resource.id
