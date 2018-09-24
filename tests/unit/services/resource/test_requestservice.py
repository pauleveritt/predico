def test_post_import2222(mocker, resourceservice):
    resourceservice.resources['a/1'] = 99
    resource = resourceservice.get_resource('a/1')
    assert 99 == resource
