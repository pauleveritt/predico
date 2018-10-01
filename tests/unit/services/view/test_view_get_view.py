def test_has_get_view(viewservice):
    assert hasattr(viewservice, 'get_view')


def test_get_view_for(
        fake_view,
        viewservice, fake_resource1,
        fake_request_class
):
    # Registrations:
    # a. Default
    # Request:
    # - resource is FakeResource
    # Expected:
    # - (a)
    fake_request = fake_request_class(resource=fake_resource1)
    result = viewservice.get_view(fake_request)
    assert 'Fake For View' in result.name


#  ---- resource: non-matching and matching

def test_get_view_nomatch_resource(
        fake_view, fakearticle_view,
        viewservice, fake_resource1,
        fake_request_class
):
    # Registrations:
    # a. Default
    # b. resource=FakeArticle
    # Request:
    # - resource is FakeResource
    # Expected:
    # - (a)
    fake_request = fake_request_class(resource=fake_resource1)
    result = viewservice.get_view(fake_request)
    assert 'Fake For View' in result.name


def test_get_view_match_resource(
        fake_view, fakearticle_view,
        viewservice, fake_article1,
        fake_request_class
):
    # Registrations:
    # a. Default
    # b. resource=FakeArticle
    # Request:
    # - resource is FakeArticle
    # Expected:
    # - (b)
    fake_request = fake_request_class(resource=fake_article1)
    result = viewservice.get_view(fake_request)
    assert 'Fake Article View' in result.name


#  ---- resourceid: non-matching and matching

def test_get_view_nomatch_resourceid(
        fake_view, fakeresourceid_view,
        viewservice, fake_article1,
        fake_request_class
):
    # Registrations:
    # a. Default
    # b. resourceid='more/article2'
    # Request:
    # - resource is 'more/article1'
    # Expected:
    # - (a)
    fake_request = fake_request_class(resource=fake_article1)
    result = viewservice.get_view(fake_request)
    assert 'Fake For View' in result.name


def test_get_view_match_resourceid(
        fake_view, fakeresourceid_view,
        viewservice, fake_article2,
        fake_request_class
):
    # Registrations:
    # a. Default
    # b. resourceid='more/article2'
    # Request:
    # - resource is 'more/article2'
    # Expected:
    # - (a)
    fake_request = fake_request_class(resource=fake_article2)
    result = viewservice.get_view(fake_request)
    assert 'Fake ResourceId View' in result.name


#  ---- parentid: non-matching and matching

def test_get_view_nomatch_parentid(
        fake_view, fakeparentid_view,
        viewservice, fake_blog1,
        fake_request_class
):
    # Registrations:
    # a. Default
    # b. parentid='more/index'
    # Request:
    # - resource is 'blog/blog1'
    # Expected:
    # - (a)
    fake_request = fake_request_class(resource=fake_blog1)
    result = viewservice.get_view(fake_request)
    assert 'Fake For View' in result.name


def test_get_view_match_parentid(
        fake_view, fakeparentid_view,
        viewservice, fake_article2,
        fake_request_class
):
    # Registrations:
    # a. Default
    # b. parentid='more/index'
    # Request:
    # - resource is 'more/article2'
    # Expected:
    # - (b)
    fake_request = fake_request_class(resource=fake_article2)
    result = viewservice.get_view(fake_request)
    assert 'Fake ParentId View' in result.name


# ---- Combination: resourceid, parentid

def test_get_view_parentid_match_resourceid(
        fake_view, fakeresourceid_view, fakeparentid_view,
        viewservice, fake_article2,
        fake_request_class
):
    # Registrations:
    # a. Default
    # b. parentid='more/index'
    # b. esourceid='more/article2'
    # Request:
    # - resource is 'more/article2'
    # Expected:
    # - (c)
    fake_request = fake_request_class(resource=fake_article2)
    result = viewservice.get_view(fake_request)
    assert 'Fake ResourceId View' in result.name


# ---- Combination: resource, parentid

def test_get_view_resource_match_parentid(
        fake_view, fakeresource_view, fakeparentid_view,
        viewservice, fake_article2,
        fake_request_class
):
    # Registrations:
    # a. Default
    # b. parentid='more/index'
    # b. resource=FakeArticle
    # Request:
    # - resource is 'more/article2'
    # Expected:
    # - (b)
    fake_request = fake_request_class(resource=fake_article2)
    result = viewservice.get_view(fake_request)
    assert 'Fake ParentId View' in result.name


# ---- Combination: all 4

def test_get_view_resource_parentid_match_resourceid(
        fake_view, fakeresource_view, fakeparentid_view,
        fakeresourceid_view,
        viewservice, fake_article2,
        fake_request_class
):
    # Registrations:
    # a. Default
    # b. parentid='more/index'
    # c. resourceid='more/article2'
    # d. resource=FakeArticle
    # Request:
    # - resource is 'more/article2'
    # Expected:
    # - (c)
    fake_request = fake_request_class(resource=fake_article2)
    result = viewservice.get_view(fake_request)
    assert 'Fake ResourceId View' in result.name
