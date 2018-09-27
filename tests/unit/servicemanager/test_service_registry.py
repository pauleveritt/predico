import dectate


def test_construction(test_registry):
    dectate.commit(test_registry)
    s = test_registry.config.services
    assert 4 == len(s)
