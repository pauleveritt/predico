def test_viewservice(viewservice):
    assert hasattr(viewservice, 'sm')
    assert hasattr(viewservice, 'registry')
    assert hasattr(viewservice, 'config')
