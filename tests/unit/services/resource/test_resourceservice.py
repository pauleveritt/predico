def test_resourceservice(resourceservice):
    assert hasattr(resourceservice, 'sm')
    assert hasattr(resourceservice, 'registry')
    assert hasattr(resourceservice, 'config')
    assert hasattr(resourceservice, 'resources')
