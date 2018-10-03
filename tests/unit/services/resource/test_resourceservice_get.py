"""

Test the various get methods on the resource service

"""


def test_has_methods(resourceservice):
    assert hasattr(resourceservice, 'get_resourceclass')
    assert hasattr(resourceservice, 'get_resource')
    assert hasattr(resourceservice, 'add_resource')


def test_add_get_resource(fake_section, resourceservice):
    resourceservice.add_resource(rtype='testsection', id='more/index',
                                 title='More Section', parentid='more/index')
    r = resourceservice.get_resource('more/index')
    assert 'more/index' == r.id
