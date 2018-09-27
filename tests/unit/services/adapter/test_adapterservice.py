def test_adapterservice(adapterservice):
    assert hasattr(adapterservice, 'sm')
    assert hasattr(adapterservice, 'registry')
    assert hasattr(adapterservice, 'config')
