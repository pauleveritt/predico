def test_has_get_view(viewservice):
    assert hasattr(viewservice, 'get_view')


def test_get_view_for(
        fakefor_view,
        viewservice, fake_resource1,
        fake_request_class
):
    # Registrations:
    # a. for_=IndexView
    # Request:
    # - resource is FakeResource
    # Expected:
    # - (a)
    fake_request = fake_request_class(resource=fake_resource1)
    result = viewservice.get_view(fake_request)
    assert 'Fake For View' in result.name


#  ---- resource: non-matching and matching

def test_get_view_for_nomatch_resource(
        fakefor_view, fakearticle_view,
        viewservice, fake_resource1,
        fake_request_class
):
    # Registrations:
    # a. for_=IndexView
    # b. for_=IndexView, resource=FakeArticle
    # Request:
    # - resource is FakeResource
    # Expected:
    # - (a)
    fake_request = fake_request_class(resource=fake_resource1)
    result = viewservice.get_view(fake_request)
    assert 'Fake For View' in result.name


def test_get_view_for_match_resource(
        fakefor_view, fakearticle_view,
        viewservice, fake_article1,
        fake_request_class
):
    # Registrations:
    # a. for_=IndexView
    # b. for_=IndexView, resource=FakeArticle
    # Request:
    # - resource is FakeArticle
    # Expected:
    # - (b)
    fake_request = fake_request_class(resource=fake_article1)
    result = viewservice.get_view(fake_request)
    assert 'Fake Article View' in result.name


#  ---- resourceid: non-matching and matching

def test_get_view_for_nomatch_resourceid(
        fakefor_view, fakeresourceid_view,
        viewservice, fake_article1,
        fake_request_class
):
    # Registrations:
    # a. for_=IndexView
    # b. for_=IndexView, resourceid='more/article2'
    # Request:
    # - resource is 'more/article1'
    # Expected:
    # - (a)
    fake_request = fake_request_class(resource=fake_article1)
    result = viewservice.get_view(fake_request)
    assert 'Fake For View' in result.name


def test_get_view_for_match_resourceid(
        fakefor_view, fakeresourceid_view,
        viewservice, fake_article2,
        fake_request_class
):
    # Registrations:
    # a. for_=IndexView
    # b. for_=IndexView, resourceid='more/article2'
    # Request:
    # - resource is 'more/article2'
    # Expected:
    # - (a)
    fake_request = fake_request_class(resource=fake_article2)
    result = viewservice.get_view(fake_request)
    assert 'Fake ResourceId View' in result.name


#  ---- parentid: non-matching and matching

def test_get_view_for_nomatch_parentid(
        fakefor_view, fakeparentid_view,
        viewservice, fake_blog1,
        fake_request_class
):
    # Registrations:
    # a. for_=IndexView
    # b. for_=IndexView, parentid='more/index'
    # Request:
    # - resource is 'blog/blog1'
    # Expected:
    # - (a)
    fake_request = fake_request_class(resource=fake_blog1)
    result = viewservice.get_view(fake_request)
    assert 'Fake For View' in result.name


def test_get_view_for_match_parentid(
        fakefor_view, fakeparentid_view,
        viewservice, fake_article2,
        fake_request_class
):
    # Registrations:
    # a. for_=IndexView
    # b. for_=IndexView, parentid='more/index'
    # Request:
    # - resource is 'more/article2'
    # Expected:
    # - (b)
    fake_request = fake_request_class(resource=fake_article2)
    result = viewservice.get_view(fake_request)
    assert 'Fake ParentId View' in result.name


# ---- Combination: for_, resourceid, parentid

def test_get_view_for_parentid_match_resourceid(
        fakefor_view, fakeresourceid_view, fakeparentid_view,
        viewservice, fake_article2,
        fake_request_class
):
    # Registrations:
    # a. for_=IndexView
    # b. for_=IndexView, parentid='more/index'
    # b. for_=IndexView, resourceid='more/article2'
    # Request:
    # - resource is 'more/article2'
    # Expected:
    # - (c)
    fake_request = fake_request_class(resource=fake_article2)
    result = viewservice.get_view(fake_request)
    assert 'Fake ResourceId View' in result.name


# ---- Combination: for_, resource, parentid

def test_get_view_for_resource_match_parentid(
        fakefor_view, fakeresource_view, fakeparentid_view,
        viewservice, fake_article2,
        fake_request_class
):
    # Registrations:
    # a. for_=IndexView
    # b. for_=IndexView, parentid='more/index'
    # b. for_=IndexView, resource=FakeArticle
    # Request:
    # - resource is 'more/article2'
    # Expected:
    # - (b)
    fake_request = fake_request_class(resource=fake_article2)
    result = viewservice.get_view(fake_request)
    assert 'Fake ParentId View' in result.name


# ---- Combination: all 4

def test_get_view_for_resource_parentid_match_resourceid(
        fakefor_view, fakeresource_view, fakeparentid_view,
        fakeresourceid_view,
        viewservice, fake_article2,
        fake_request_class
):
    # Registrations:
    # a. for_=IndexView
    # b. for_=IndexView, parentid='more/index'
    # c. for_=IndexView, resourceid='more/article2'
    # d. for_=IndexView, resource=FakeArticle
    # Request:
    # - resource is 'more/article2'
    # Expected:
    # - (c)
    fake_request = fake_request_class(resource=fake_article2)
    result = viewservice.get_view(fake_request)
    assert 'Fake ResourceId View' in result.name
