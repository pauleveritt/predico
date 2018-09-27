def test_requestservice(requestservice):
    assert hasattr(requestservice, 'sm')
    assert hasattr(requestservice, 'registry')
    assert hasattr(requestservice, 'config')
